import json
import os
from datetime import datetime, timezone
from glob import glob


def save_results(pipeline_name: str, results: list[dict], results_dir: str = "results") -> str:
    """Write a run's results to a local JSON file. Returns the file path."""
    os.makedirs(results_dir, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{pipeline_name}_{timestamp}.json"
    path = os.path.join(results_dir, filename)

    with open(path, "w") as f:
        json.dump(results, f, indent=2)

    return path


def load_latest_results(pipeline_name: str, results_dir: str = "results") -> list[dict]:
    """Return the results list from the most recent run of a pipeline, or [] if none exist."""
    pattern = os.path.join(results_dir, f"{pipeline_name}_*.json")
    files = sorted(glob(pattern))

    if not files:
        return []

    with open(files[-1]) as f:
        return json.load(f)
