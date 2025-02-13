from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from hydrogram.types import CallbackQuery, Message

if TYPE_CHECKING:
    from hydrogram.types import Chat, User


def _get_chat(update) -> Optional[Chat]:
    if isinstance(update, Message):
        return update.chat
    return (
        update.message.chat
        if isinstance(update, CallbackQuery)
        else None
    )

def _get_user(update) -> Optional[User | Chat]:
    if isinstance(update, Message):
        return (
            update.from_user
            if update.from_user
            else update.sender_chat or None
        )
    return (
        update.from_user
        if isinstance(update, CallbackQuery)
        else None
    )

def _get_message(update) -> Optional[Message]:
    if isinstance(update, CallbackQuery):
        return update.message
    return update if isinstance(update, Message) else None

def _get_callback_data(update) -> Optional[str | bytes]:
    return (
        update.data
        if isinstance(update, CallbackQuery)
        else None
    )

def extract_data(update) -> tuple:
    return (
        _get_chat(update),
        _get_user(update),
        _get_message(update),
        _get_callback_data(update)
    )
