import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logger(
    log_dir: Path = Path("logs"),
    log_level: int = logging.INFO,
    log_format: str = "[%(asctime)s] %(levelname)s in %(name)s at line %(lineno)d: %(message)s",
) -> logging.Logger:
    """
    Set up a logger that writes timestamped log files in the given directory.

    Args:
        log_dir (Path): Directory where log files will be stored.
        log_level (int): Minimum logging level to capture (default: logging.INFO).
        log_format (str): Format string for log messages.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Ensure the log directory exists
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create a unique log file name with timestamp
    log_file_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".log"
    log_file_path = log_dir / log_file_name

    # Configure logging
    logging.basicConfig(
        filename=log_file_path,
        format=log_format,
        level=log_level,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file_path}")
    return logger
