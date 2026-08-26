# NZ Data Engineer Journey

This repository is organized as a learning-to-portfolio progression, with one flagship project intended to represent senior-level data engineering thinking.

## Flagship Project

The main portfolio project is `domains/analytics_spark_project`.

It demonstrates:

- layered lakehouse-style architecture with raw, silver, gold, and quality outputs
- PySpark DataFrame transformations and window-based sessionization
- Spark SQL analytics for business-facing gold tables
- Python project structure with clear orchestration, reusable utilities, and configuration boundaries
- data quality validation, referential checks, and output auditing

## Repository Layout

- `domains/analytics_spark_project`: flagship PySpark analytics platform
- `domains/user_profile`: smaller modular Python ETL exercise
- `domains/spark_user_activity`: smaller Spark transformation exercise
- `business/`: early-stage practice scripts kept as historical learning material
- `tests/`: unit tests and project-level checks

## Recommended Interview Narrative

Use the flagship project to explain:

1. How raw interaction data is cleaned, validated, enriched, and modeled into analytics tables.
2. Why some transformations are written in the DataFrame API while gold reporting tables are expressed in SQL.
3. How data quality gates are enforced before trusting downstream metrics.
4. How the project can be extended toward orchestration, CI, and cloud deployment.

## Quick Start

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python -m domains.analytics_spark_project.jobs.generate_data
python -m domains.analytics_spark_project.jobs.run_pipeline
pytest -q
```

## Next Steps

To make this repo even stronger for a senior data engineer job search, the next logical additions are Airflow orchestration, CI checks, and containerized local execution.
