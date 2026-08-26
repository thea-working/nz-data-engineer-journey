import argparse
import json
import logging
from pathlib import Path

from domains.analytics_spark_project.pipeline.analytics_pipeline import run_pipeline
from domains.analytics_spark_project.pipeline.settings import PipelineSettings
from domains.analytics_spark_project.utils.spark_session import create_spark
from infrastructure.logging_config import setup_logging


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the user behavior analytics pipeline"
    )
    parser.add_argument(
        "--top-n-content",
        type=int,
        default=10,
        help="Number of top content records to keep per category",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_root = Path(__file__).resolve().parent.parent
    log_file = project_root / "pipeline.log"
    setup_logging(log_file=log_file, log_level="INFO")

    spark = create_spark()
    try:
        settings = PipelineSettings.from_project_root(
            project_root=project_root,
            top_n_content=args.top_n_content,
        )
        summary = run_pipeline(spark, settings=settings)
        logging.getLogger(__name__).info(
            "Pipeline outputs: %s", json.dumps(summary, indent=2)
        )
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
