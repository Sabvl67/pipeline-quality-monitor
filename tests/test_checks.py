from sqlalchemy import text

from checks.null_rate import NullRateCheck
from checks.row_count_drift import RowCountDriftCheck


class TestNullRateCheck:
    def test_passes_when_null_rate_below_threshold(self, connection):
        check = NullRateCheck("test_pipeline", "orders", "customer_id", threshold=0.3)
        result = check.run(connection)

        assert result["status"] == "PASS"
        assert result["observed_value"] == 0.2
        assert result["check_name"] == "null_rate"
        assert result["table"] == "orders"
        assert result["column"] == "customer_id"

    def test_fails_when_null_rate_above_threshold(self, connection):
        check = NullRateCheck("test_pipeline", "orders", "customer_id", threshold=0.1)
        result = check.run(connection)

        assert result["status"] == "FAIL"
        assert result["observed_value"] == 0.2

    def test_warns_on_empty_table(self, connection):
        connection.execute(text("DELETE FROM orders"))
        connection.commit()

        check = NullRateCheck("test_pipeline", "orders", "customer_id", threshold=0.1)
        result = check.run(connection)

        assert result["status"] == "WARN"
        assert result["observed_value"] == 0.0


class TestRowCountDriftCheck:
    def test_passes_when_drift_below_threshold(self, connection):
        # 10 current rows vs 9 previous = ~11% drift
        check = RowCountDriftCheck("test_pipeline", "orders", threshold=0.2, previous_count=9)
        result = check.run(connection)

        assert result["status"] == "PASS"
        assert result["observed_value"] == 10

    def test_fails_when_drift_above_threshold(self, connection):
        # 10 current rows vs 5 previous = 100% drift
        check = RowCountDriftCheck("test_pipeline", "orders", threshold=0.2, previous_count=5)
        result = check.run(connection)

        assert result["status"] == "FAIL"
        assert result["observed_value"] == 10

    def test_warns_when_no_previous_count(self, connection):
        check = RowCountDriftCheck("test_pipeline", "orders", threshold=0.2, previous_count=None)
        result = check.run(connection)

        assert result["status"] == "WARN"
        assert result["observed_value"] == 10
