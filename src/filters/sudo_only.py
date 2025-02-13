from __future__ import annotations

from collections.abc import Generator
from typing import TYPE_CHECKING, Any

from hydrogram.filters import Filter
from hydrogram.types import CallbackQuery
from loguru import logger

from src.config import ConfigManager

if TYPE_CHECKING:
    from hydrogram import Client
    from hydrogram.types import Update


def load_sudoers() -> set[int]:
    sudoers = ConfigManager.get("telegram", "SUDOERS")

    if not sudoers:
        raise ValueError(
            'The `SUDOERS` list was not loaded correctly.'
            'Please check your configuration file.'
        )

    if not isinstance(sudoers, list):
        raise ValueError(
            'The `SUDOERS` list must be a list.'
            'Please check your configuration file.'
        )

    if not all(isinstance(user_id, int) for user_id in sudoers):
        raise ValueError(
            'The `SUDOERS` list must contain only integers.'
            'Please check your configuration file.'
        )

    return set(sudoers)


SUDOERS = load_sudoers()


class SudoOnly(Filter):
    __slots__ = ("client", "update")

    def __init__(self, client: Client, update: Update) -> None:
        self.client = client
        self.update = update

    async def __call__(self) -> bool:
        update = self.update
        is_callback = isinstance(update, CallbackQuery)
        message = update.message if is_callback else update
        user = update.from_user

        if user.id in SUDOERS:
            logger.debug("[Filters/Sudo] Access granted.", user=user.id, chat=message.chat.id)
            return True

        logger.warning(
            "[Filters/Sudo] Unauthorized access attempt.", user=user.id, chat=message.chat.id
        )
        return False

    def __await__(self) -> Generator[Any, Any, bool]:
        return self.__call__().__await__()
