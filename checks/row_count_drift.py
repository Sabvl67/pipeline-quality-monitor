from sqlalchemy import text
from sqlalchemy.engine import Connection

from checks.base import Check


class RowCountDriftCheck(Check):
    """Fails if the row count has drifted from the previous run by more than a threshold percentage."""

    name = "row_count_drift"

    def __init__(self, pipeline_name: str, table: str, threshold: float, previous_count: int | None):
        super().__init__(pipeline_name, table)
        self.threshold = threshold
        self.previous_count = previous_count

    def run(self, connection: Connection) -> dict:
        current_count = connection.execute(
            text(f"SELECT COUNT(*) FROM {self.table}")
        ).scalar()

        if not self.previous_count:
            return self.build_result("WARN", current_count, self.threshold)

        drift = abs(current_count - self.previous_count) / self.previous_count
        status = "FAIL" if drift > self.threshold else "PASS"
        return self.build_result(status, current_count, self.threshold)
