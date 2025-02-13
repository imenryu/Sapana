from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING

from hydrogram.types import CallbackQuery
from loguru import logger
from pyrate_limiter import Duration, Limiter, Rate
from pyrate_limiter.exceptions import BucketFullException

if TYPE_CHECKING:
    from hydrogram import Client
    from hydrogram.types import Update

messages_per_window = 1
window_seconds = 2
rate = Rate(
          messages_per_window,
          Duration.SECOND * window_seconds,
       )
limiter = Limiter(rate)


def rate_limit():
    def decorator(callback):
        @wraps(callback)
        async def wrapper(client: Client, update: Update):
            user_id = f'{update.from_user.id}'
            try:
                limiter.try_acquire(user_id)
            except BucketFullException:
                logger.warning(
                    f'Rate limit exceeded for user {user_id}. Allowed {messages_per_window} updates in {window_seconds} seconds.'
                )
                if isinstance(update, CallbackQuery):
                    await update.answer(text='wait for a moment.', show_alert=True)
            else:
                await callback(client, update)
        return wrapper
    return decorator
