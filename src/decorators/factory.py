from __future__ import annotations
from collections.abc import Callable
from typing import TYPE_CHECKING, ClassVar, Any

from src.handlers.callback_query_handler import CustomCallbackQueryHandler
from src.handlers.error_handler import CustomErrorHandler
from src.handlers.message_handler import CustomMessageHandler

if TYPE_CHECKING:
    from hydrogram.filters import Filter
    from hydrogram.handlers.handler import Handler


class Factory:
    __slots__: str = "update_name"

    updates_observed: ClassVar[dict[str, type[Handler]]] = {
        "callback_query": CustomCallbackQueryHandler,
        "error": CustomErrorHandler,
        "message": CustomMessageHandler,
    }

    def __init__(self, update_name: str) -> None:
        """
        Initialize the Factory with a specific update name.
        
        :param update_name: The type of update (e.g., 'message', 'error').
        """
        self.update_name: str = update_name

    def __call__(self, filters: Filter | None = None, group: int = 0) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """
        A decorator generator that assigns a handler to the decorated function.

        :param filters: A filter to apply to the handler (optional).
        :param group: The priority group for the handler.
        :return: A decorator function.
        """
        def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
            """
            The decorator function that associates a handler with the function.

            :param func: The function to decorate.
            :return: The decorated function.
            """
            if not hasattr(func, "handlers"):
                func.handlers: list[tuple[Handler, int]] = []  # Define the type explicitly

            if (handler_class := self.updates_observed.get(self.update_name)) is None:
                raise ValueError(f'No handler found for update: {self.update_name}')

            # Add the handler and group to the function's handlers list
            func.handlers.append({'handler': handler_class(func, filters), 'group': group})  # type: ignore[arg-type]

            return func

        return wrapper
