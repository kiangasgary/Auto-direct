import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler

def setup_logger() -> logging.Logger:
    """
    Set up application logging with both file and console handlers
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Get log level from environment variable or default to INFO
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    numeric_level = getattr(logging, log_level, logging.INFO)

    # Create logger
    logger = logging.getLogger("instagram_dm_automation")
    logger.setLevel(numeric_level)

    # Remove existing handlers if any
    logger.handlers = []

    # Create formatters
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_formatter = logging.Formatter("%(message)s")

    # File handler (with rotation)
    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=10_000_000,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(numeric_level)

    # Console handler (using Rich for better formatting)
    console_handler = RichHandler(rich_tracebacks=True)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(numeric_level)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Log initial setup
    logger.info("Logger initialized")
    logger.debug(f"Log level set to {log_level}")

    return logger 