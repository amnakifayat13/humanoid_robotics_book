import logging
import sys
from typing import Optional
from datetime import datetime


class LoggerSetup:
    """
    Centralized logging setup for the data ingestion pipeline.
    """

    @staticmethod
    def setup_logging(name: str = "data_ingestion", level: int = logging.INFO) -> logging.Logger:
        """
        Set up logging with both console and file handlers.

        Args:
            name: Name of the logger
            level: Logging level (default: INFO)

        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Prevent adding multiple handlers if logger already exists
        if logger.handlers:
            return logger

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(console_handler)

        return logger


def log_error(error: Exception, context: str = "") -> None:
    """
    Log an error with context information.

    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
    """
    logger = LoggerSetup.setup_logging()
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)


def log_info(message: str, context: str = "") -> None:
    """
    Log an informational message.

    Args:
        message: The message to log
        context: Additional context
    """
    logger = LoggerSetup.setup_logging()
    log_msg = f"{context}: {message}" if context else message
    logger.info(log_msg)


class ProcessingError(Exception):
    """
    Custom exception for processing errors in the data pipeline.
    """

    def __init__(self, message: str, error_code: Optional[str] = None, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.original_error = original_error
        self.timestamp = datetime.now()

    def __str__(self):
        base_msg = f"ProcessingError[{self.error_code}]: {self.message}"
        if self.original_error:
            base_msg += f" (caused by: {type(self.original_error).__name__}: {str(self.original_error)})"
        return base_msg