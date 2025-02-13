from collections.abc import Mapping
from typing import Optional, Union, Any

from .base import GulambiError, ErrorContext


class UnknownError(GulambiError):
    """
    Raised for unknown error.
    """

    def __init__(self,
        message: str,
        context: Optional[Union[Mapping[str, Any], ErrorContext]] = None,
        user_friendly_message: Optional[str] = None
    ):
        super().__init__(
            message, 6969, context,
            user_friendly_message
        )
        
class ConfigError(GulambiError):
    """
    Raised for configuration error.
    """

    def __init__(self,
        message: str,
        context: Optional[Union[Mapping[str, Any], ErrorContext]] = None,
        user_friendly_message: Optional[str] = None
    ):
        super().__init__(
            message, 6901, context,
            user_friendly_message
        )

class DatabaseError(GulambiError):
    """
    Raised for database error.
    """

    def __init__(self,
        message: str,
        context: Optional[Union[Mapping[str, Any], ErrorContext]] = None,
        user_friendly_message: Optional[str] = None
    ):
        super().__init__(
            message, 6902, context,
            user_friendly_message
        )

class RouterError(GulambiError):
    """
    Raised for router (decorators) error.
    """

    def __init__(self,
        message: str,
        context: Optional[Union[Mapping[str, Any], ErrorContext]] = None,
        user_friendly_message: Optional[str] = None
    ):
        super().__init__(
            message, 6903, context,
            user_friendly_message
        )

class CommandError(GulambiError):
    """
    Raised for command error.
    """

    def __init__(self,
        message: str,
        context: Optional[Union[Mapping[str, Any], ErrorContext]] = None,
        user_friendly_message: Optional[str] = None
    ):
        super().__init__(
            message, 6904, context,
            user_friendly_message
        )

class MalformedQueryError(GulambiError):
    """
    Raised for malformed query error.
    """

    def __init__(self,
        message: str,
        context: Optional[Union[Mapping[str, Any], ErrorContext]] = None,
        user_friendly_message: Optional[str] = None
    ):
        super().__init__(
            message, 6905, context,
            user_friendly_message
        )
        
class RegexError(GulambiError):
    """
    Raised for regex error.
    """

    def __init__(self,
        message: str,
        context: Optional[Union[Mapping[str, Any], ErrorContext]] = None,
        user_friendly_message: Optional[str] = None
    ):
        super().__init__(
            message, 6906, context,
            user_friendly_message
        )
        
class LocalesError(GulambiError):
    """
    Raised for locales error.
    """

    def __init__(self,
        message: str,
        context: Optional[Union[Mapping[str, Any], ErrorContext]] = None,
        user_friendly_message: Optional[str] = None
    ):
        super().__init__(
            message, 6907, context,
            user_friendly_message
        )
