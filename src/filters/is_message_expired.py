from __future__ import annotations

from collections.abc import Generator
from contextlib import suppress
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

from hydrogram.filters import Filter
from hydrogram.errors import MessageDeleteForbidden, MessageNotModified
from hydrogram.types import CallbackQuery
from loguru import logger

if TYPE_CHECKING:
    from hydrogram import Client
    from hydrogram.types import Update


class IsMessageExpired(Filter):
    __slots__ = ("client", "update")

    def __init__(self, client: Client, update: Update) -> None:
        self.client = client
        self.update = update

    async def __call__(self) -> bool:
        update = self.update
        if isinstance(update, CallbackQuery):
            user = update.from_user
            chat = update.message.chat
            deleted = False

            now = datetime.now()
            two_days_ago = timedelta(days=2) - timedelta(minutes=2)
            date_to_check = update.message.date
  
            if (now - date_to_check) >= two_days_ago:
                logger.debug("[Filters/Message-Expired] - Yes", user=user.id, chat=chat.id)
                await update.answer(text='Callback Expired.') 

                with suppress(MessageDeleteForbidden):
                    await update.message.delete()
                    deleted = True

                if not deleted:
                    with suppress(MessageNotModified):
                        await update.edit_message_text(text='Message Expired.')
                return False

            logger.debug(
                "[Filters/Message-Expired] - No", user=user.id, chat=chat.id
            )
            return True

    def __await__(self) -> Generator[Any, Any, bool]:
        return self.__call__().__await__()
