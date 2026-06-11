from abc import ABC, abstractmethod
from datetime import datetime, timezone

from sqlalchemy.engine import Connection


class Check(ABC):
    """Base class for all data quality checks."""

    #: Set by subclasses to identify the check type in results (e.g. "null_rate")
    name: str = "check"

    def __init__(self, pipeline_name: str, table: str, column: str | None = None):
        self.pipeline_name = pipeline_name
        self.table = table
        self.column = column

    @abstractmethod
    def run(self, connection: Connection) -> dict:
        """Execute the check against the given connection and return a result dict."""
        raise NotImplementedError

    def build_result(self, status: str, observed_value, threshold) -> dict:
        return {
            "check_name": self.name,
            "pipeline_name": self.pipeline_name,
            "table": self.table,
            "column": self.column,
            "status": status,
            "observed_value": observed_value,
            "threshold": threshold,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
