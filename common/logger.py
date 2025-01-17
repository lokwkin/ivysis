import logging
from logging.handlers import RotatingFileHandler
import sys


def setup_logging(default_level=logging.INFO):
    """Initialize the root logger with default configuration"""
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s [%(name)s] %(levelname)s - %(message)s'
    )

    # App logger
    app_logger = logging.getLogger('app')
    app_logger.setLevel(default_level)

    # File handler
    file_handler = RotatingFileHandler(
        'app.log',
        maxBytes=10*1024*1024,
        backupCount=5
    )
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)

    # Add handlers to root logger
    app_logger.addHandler(file_handler)
    app_logger.addHandler(console_handler)


def get_logger(name=None):
    """Get a logger with the specified name"""
    return logging.getLogger(f"app.{name or __name__}")


# Initialize logging when the module is imported
setup_logging()
