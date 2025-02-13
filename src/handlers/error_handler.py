from __future__ import annotations

from typing import TYPE_CHECKING

from hydrogram.handlers import ErrorHandler

from .base import BaseHandler

if TYPE_CHECKING:
    from hydrogram import Client
    from hydrogram.types import Update


class CustomErrorHandler(ErrorHandler, BaseHandler):
    async def check(self, client: Client, update: Update, exception: Exception) -> bool:
        if not isinstance(exception, self.exceptions):
            return False

        await self.callback(client, update, exception)
        return True
