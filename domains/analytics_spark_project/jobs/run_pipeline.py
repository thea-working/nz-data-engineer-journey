import logging
from pathlib import Path

from domains.analytics_spark_project.pipeline.analytics_pipeline import \
    run_pipeline
from domains.analytics_spark_project.utils.spark_session import create_spark
from infrastructure.logging_config import setup_logging


def main():
    spark = create_spark()
    log_file = Path(__file__).resolve().parent.parent / "pipeline.log"
    setup_logging(str(log_file), "INFO")
    logger = logging.getLogger(__name__)

    try:

        logger.info("analytics spark project pipeline started")

        run_pipeline(spark)

        logger.info("analytics spark project finished successfully")

    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}")

    spark.stop()


if __name__ == "__main__":
    main()
