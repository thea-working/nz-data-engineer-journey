import logging
from pathlib import Path

from business.day8_log_processors.user_log_processor import UserLogProcessor
from infrastructure.logging_config import setup_logging


def main():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / 'data'
    setup_logging(
        log_file=str(base_dir / 'app.log'),
        log_level='INFO'
    )
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"User logs processing started")
        input_file = data_dir / 'user_logs.json'
        output_path = data_dir

        processor = UserLogProcessor(input_file, output_path)
        processor.run()
        logger.info(f"User logs processing finished successfully")

    except Exception as e:
        logger.exception(f'User log processing failed: {e}')


if __name__ == "__main__":
    main()
