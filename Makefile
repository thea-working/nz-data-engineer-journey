.PHONY: setup format lint test generate run

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -e '.[dev]'

format:
	python3 -m black domains tests infrastructure

lint:
	python3 -m ruff check domains tests infrastructure

test:
	python3 -m pytest -q

generate:
	python3 -m domains.analytics_spark_project.jobs.generate_data

run:
	python3 -m domains.analytics_spark_project.jobs.run_pipeline
