import sys
import traceback
from src.logger import logging
from types import TracebackType
from typing import Optional, Type


def format_error_message(error: Exception, tb: Optional[TracebackType]) -> str:
    """
    Build a detailed error message including the file name, line number, and error text.

    Args:
        error (Exception): The actual exception instance that was raised.
        tb (Optional[TracebackType]): The traceback object from sys.exc_info().

    Returns:
        str: A formatted, human-readable error message.
    """
    if tb is None:
        return str(error)  # No traceback available, just return the error text.

    file_name = tb.tb_frame.f_code.co_filename
    line_number = tb.tb_lineno
    return (
        f"Error occurred in python script with the file name [{file_name}] "
        f"at the line [{line_number}]: {error}"
    )


class CustomException(Exception):
    """
    A custom exception that provides detailed error location information.
    """

    def __init__(
        self,
        error: Exception,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        tb: Optional[TracebackType] = None,
    ):
        """
        Initialize the custom exception with detailed error information.

        Args:
            error (Exception): The original exception instance.
            exc_type (Optional[Type[BaseException]]): The type of the original exception.
            exc_value (Optional[BaseException]): The value of the original exception.
            tb (Optional[TracebackType]): The traceback object of the original exception.
        """
        super().__init__(str(error))
        self.detailed_message = format_error_message(error, tb)

    def __str__(self) -> str:
        return self.detailed_message
