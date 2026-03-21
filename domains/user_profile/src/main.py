import json
import logging
from pathlib import Path

from infrastructure.logging_config import setup_logging

from .analyzer import analyze_users_optimized
from .cleaner import clean_users
from .loader import load_users_from_csv
from .writer import save_result

# user profile data pipeline


def load_config():
    config_path = Path(__file__).resolve().parent.parent / "config.json"
    with open(config_path, "r") as f:
        return json.load(f)


def main():
    config = load_config()
    base_dir = Path(__file__).resolve().parent.parent

    # initial logging
    setup_logging(
        log_file=base_dir / config["log_file"],
        log_level=config.get("log_level", "INFO"),
    )
    logger = logging.getLogger(__name__)

    try:
        logger.info("User profile pipeline started")
        input_file = base_dir / config["input_file"]
        output_file = base_dir / config["output_file"]

        # load user data from csv file
        users_data = load_users_from_csv(input_file)
        # clean users data according to rules
        cleaned_users = clean_users(users_data)
        # calculate metrics
        stats = analyze_users_optimized(cleaned_users)
        # write result to file
        save_result(stats, output_file)

        logger.info("User profile pipeline finished successfully")
    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}")


if __name__ == "__main__":
    main()
