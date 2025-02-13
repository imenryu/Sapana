from __future__ import annotations

from typing import TYPE_CHECKING

from hydrogram.handlers import CallbackQueryHandler

from .base import BaseHandler

if TYPE_CHECKING:
    from hydrogram import Client
    from hydrogram.types import CallbackQuery


class CustomCallbackQueryHandler(CallbackQueryHandler, BaseHandler):
    async def check(self, client: Client, callback: CallbackQuery) -> None:
        return await self._check_and_handle(client, callback)
