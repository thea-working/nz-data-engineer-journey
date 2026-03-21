import logging
from pathlib import Path

from business.day10_api_post_pipeline.api_ingestion import APIIngestion
from business.day10_api_post_pipeline.api_post_pipeline import APIPostPipeline
from infrastructure.logging_config import setup_logging


def main():
    base_dir = Path(__file__).resolve().parent.parent
    setup_logging(log_file=str(base_dir / "app.log"), log_level="INFO")
    logger = logging.getLogger(__name__)
    output_dir = base_dir / "data"
    json_file = output_dir / "api_posts.json"

    try:
        api_url = "https://jsonplaceholder.typicode.com/posts"
        # load
        ingestion = APIIngestion(api_url)
        data = ingestion.fetch_data()

        # output
        ingestion.save_json(data, output_dir)

        pipeline = APIPostPipeline(json_file, output_dir)
        pipeline.run()

        logger.info("Fetching and processing API data finished successfully")

    except Exception as e:
        logger.exception(f"Fetching and processing API data failed: {e}")


if __name__ == "__main__":
    main()
