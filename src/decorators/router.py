from typing import Self

from .factory import Factory
from src.errors import RouterError


class Router:
    __slots__ = ("callback_query", "error", "message")

    def __init__(self) -> None:
        self.message: Factory = Factory("message")
        self.callback_query: Factory = Factory("callback_query")
        self.error: Factory = Factory("error")

    def __getattr__(self, name: str) -> Self:
        msg = f"Event of type '{name}' is not supported"
        raise RouterError(msg)
