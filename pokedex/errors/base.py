import traceback
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Optional, Union, Any

from loguru import logger 

@dataclass(frozen=True)
class ErrorContext:
    """
    Represents additional metadata or context for debugging errors.

    Attributes:
        details (Mapping[str, Any]): A dictionary of contextual data.
    """
    details: Mapping[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        """
        String representation of the context for debugging.
        """
        return ', '.join(f'{key}={value}' for key, value in self.details.items())


class PokedexError(Exception):
    """
    PokedexError - Base class for all custom application-specific exceptions.

    Attributes:
        message (str): A detailed error message.
        error_code (Optional[int]): An optional code for categorizing the error.
        context (Optional[ErrorContext]): Additional metadata for debugging.
        user_friendly_message (Optional[str]): Optional message suitable for end-users.
    """
    def __init__(
        self,
        message: str,
        error_code: Optional[int] = None,
        context: Optional[Union[Mapping[str, Any], ErrorContext]] = None,
        user_friendly_message: Optional[str] = None,
    ):
        super().__init__(message)
        self.message: str = message
        self.error_code: Optional[int] = error_code
        self.context: ErrorContext = (
            context if isinstance(context, ErrorContext) else ErrorContext(context or {})
        )
        self.user_friendly_message: str = (
            user_friendly_message or 'An unexpected error occurred. Please try again later.'
        )

        self.log_error()

    def __str__(self) -> str:
        """
        Return a detailed string representation of the error, including error code and context.
        """
        error_str = f'[{self.error_code}] {self.message}' if self.error_code else self.message
        if self.context.details:
            error_str += f' | Context: {self.context}'
        return error_str

    def log_error(self) -> None:
        """
        Logs the error details with the message, context, and traceback.
        """
        logger.exception(f'Error: {self}\n\nTraceback: {traceback.format_exc()}')
