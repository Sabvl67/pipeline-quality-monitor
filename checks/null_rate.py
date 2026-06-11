from sqlalchemy import text
from sqlalchemy.engine import Connection

from checks.base import Check


class NullRateCheck(Check):
    """Fails if the percentage of NULL values in a column exceeds a threshold."""

    name = "null_rate"

    def __init__(self, pipeline_name: str, table: str, column: str, threshold: float):
        super().__init__(pipeline_name, table, column)
        self.threshold = threshold

    def run(self, connection: Connection) -> dict:
        total = connection.execute(
            text(f"SELECT COUNT(*) FROM {self.table}")
        ).scalar()

        if total == 0:
            return self.build_result("WARN", 0.0, self.threshold)

        nulls = connection.execute(
            text(f"SELECT COUNT(*) FROM {self.table} WHERE {self.column} IS NULL")
        ).scalar()

        null_rate = nulls / total
        status = "FAIL" if null_rate > self.threshold else "PASS"
        return self.build_result(status, null_rate, self.threshold)
