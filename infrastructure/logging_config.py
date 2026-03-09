# logging information
import logging
import logging.config
from pathlib import Path


def setup_logging(log_file: str, log_level: str = "INFO"):
    """
    Setup logging configuration.

    :param log_file: 日志文件路径
    :param log_level: 日志级别
    """

    # 确保日志目录存在
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,

        "formatters": {
            "standard": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | "
                          "%(filename)s:%(lineno)d | %(message)s"
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "standard",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": log_level,
                "formatter": "standard",
                "filename": str(log_file),
                "maxBytes": 5 * 1024 * 1024,  # 5 MB
                "backupCount": 3,
                "encoding": "utf-8"
            }
        },

        "root": {
            "level": log_level,
            "handlers": ["console", "file"]
        }
    }

    logging.config.dictConfig(logging_config)