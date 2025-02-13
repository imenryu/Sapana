from __future__ import annotations

import inspect
from typing import Optional, TYPE_CHECKING, Union

from hydrogram.types import CallbackQuery, Message

if TYPE_CHECKING:
    from collections.abc import Callable
    
    from hydrogram import Client
    from hydrogram.filters import Filter
    from hydrogram.types import Update, User


class BaseHandler:
    __slots__ = ("callback", "filters")

    def __init__(self, callback: Callable, filters: Filter = None) -> None:
        self.callback = callback
        self.filters = filters

    @staticmethod
    async def _extract_message_and_user(update: Update) -> tuple[Optional[Union[Message, User]]]:
        if isinstance(update, CallbackQuery):
            return update.message, update.from_user
        if isinstance(update, Message):
            return update, update.from_user
        return None, None

    async def _process_update(self, client: Client, update: Update) -> Optional[Callable]:
        message, user = await self._extract_message_and_user(update)
        if not message:
            return None

        if user and not user.is_bot and message:
            return await self.callback(client, update)
        return None

    async def _validate(self, client: Client, update: Update) -> bool:
        message, _ = await self._extract_message_and_user(update)
        if not message or not callable(self.filters):
            return False

        if inspect.iscoroutinefunction(self.filters.__call__):
            return await self.filters(client, update)
        return await client.loop.run_in_executor(
            client.executor, self.filters, client, update
        )  # type: ignore

    async def _check_and_handle(self, client: Client, update: Update) -> None:
        if await self._validate(client, update):
            await self._process_update(client, update)
