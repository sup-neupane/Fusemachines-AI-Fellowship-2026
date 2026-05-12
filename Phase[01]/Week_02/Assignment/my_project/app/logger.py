import logging
import os
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv  # type:ignore

load_dotenv()


def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Root logger configuration — propagates to all child loggers
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.StreamHandler(),                         
            RotatingFileHandler(                              
                "app.log",
                maxBytes=5 * 1024 * 1024,                   
                backupCount=3,
                encoding="utf-8"
            )
        ]
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)