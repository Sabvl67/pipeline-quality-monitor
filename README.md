# pipeline-quality-monitor

The Problem

ETL pipelines fail in two ways: loudly, or silently.

Loud failures are easy — the job errors out and someone gets paged. Silent failures are the expensive ones. A pipeline completes successfully but delivers a table where 40% of a critical column is suddenly null. A schema change upstream drops a column. A daily load that normally brings in 50,000 rows brings in 3. Nobody notices until an analyst spots a wrong number in a report — or worse, a stakeholder does.

This tool runs after every pipeline execution, validates the output data against configurable rules, and tracks results over time so you can see quality trends, not just point-in-time snapshots.


What It Does


Connects to any SQL source (PostgreSQL, SQL Server, SQLite, Azure SQL) via SQLAlchemy
Runs a configurable suite of data quality checks against target tables
Stores check results as JSON in Azure Blob Storage after each run
Surfaces a Power BI Desktop dashboard showing health trends, failure history, and top offending tables
Runs automatically on a schedule via Azure Functions timer trigger or GitHub Actions
