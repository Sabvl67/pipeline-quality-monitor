import yaml
from sqlalchemy import create_engine

from checks.null_rate import NullRateCheck
from checks.row_count_drift import RowCountDriftCheck
from runner.store import load_latest_results, save_results

CHECK_REGISTRY = {
    "null_rate": NullRateCheck,
    "row_count_drift": RowCountDriftCheck,
}


def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def build_check(check_config: dict, pipeline_name: str, previous_results: list[dict]):
    check_type = check_config["type"]
    check_class = CHECK_REGISTRY[check_type]
    table = check_config["table"]

    if check_type == "null_rate":
        return NullRateCheck(
            pipeline_name=pipeline_name,
            table=table,
            column=check_config["column"],
            threshold=check_config["threshold"],
        )

    if check_type == "row_count_drift":
        previous_count = _find_previous_row_count(previous_results, table)
        return RowCountDriftCheck(
            pipeline_name=pipeline_name,
            table=table,
            threshold=check_config["threshold"],
            previous_count=previous_count,
        )

    raise ValueError(f"Unknown check type: {check_type}")


def _find_previous_row_count(previous_results: list[dict], table: str) -> int | None:
    for result in previous_results:
        if result["check_name"] == "row_count_drift" and result["table"] == table:
            return result["observed_value"]
    return None


def run_pipeline(pipeline_config: dict, results_dir: str = "results") -> list[dict]:
    pipeline_name = pipeline_config["name"]
    engine = create_engine(pipeline_config["connection"])
    previous_results = load_latest_results(pipeline_name, results_dir)

    results = []
    with engine.connect() as connection:
        for check_config in pipeline_config["checks"]:
            check = build_check(check_config, pipeline_name, previous_results)
            results.append(check.run(connection))

    save_results(pipeline_name, results, results_dir)
    return results


def run_all(config_path: str, results_dir: str = "results") -> dict[str, list[dict]]:
    config = load_config(config_path)
    return {
        pipeline["name"]: run_pipeline(pipeline, results_dir)
        for pipeline in config["pipelines"]
    }


if __name__ == "__main__":
    all_results = run_all("config/pipelines.yml")
    for pipeline_name, results in all_results.items():
        print(f"\n{pipeline_name}:")
        for result in results:
            print(f"  {result['check_name']} ({result['table']}): {result['status']}")
