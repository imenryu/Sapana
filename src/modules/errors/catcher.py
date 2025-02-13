import html
import sys
import traceback
from typing import Optional, Union

from hydrogram.errors import ChatWriteForbidden
from loguru import logger

from src import constants
from src.config import ConfigManager
from src.decorators import router
from src.utils.keyboard import Keyboard
from src.utils.paspybin import paste
from src.utils.utility import delete_if_exists
from ._utils import extract_data


async def log_exception(
    client, exception, pretty_message: str, paste_url: str = None
) -> None:
    text = ('An unexpected error occurred while'
            f' processing this update! :/\n\n{exception}')
    
    if paste_url:
        keyboard = Keyboard([
          [(
              'Pastebin',
              f'pastebin.com/{paste_url}',
              'url'
          )]
        ])
        await client.send_message(
            ConfigManager.get('telegram', 'LOGS_CHAT'),
            text=text, reply_markup=keyboard
        )
    else:
        filename = 'error.txt'
        try:
            async with aiofiles.open(filename, 'w') as f:
                await f.write(pretty_message)
            await client.send_document(
                chat_id=ConfigManager.get('telegram', 'LOGS_CHAT'),
                document=filename,
                caption=text
            )
        finally:
            delete_if_exists(filename)
        
    
@router.error()
async def handle_error(client, update, exception) -> None:
    chat, user, message, callback_data = extract_data(update)
    
    if isinstance(exception, ChatWriteForbidden) and chat:
        logger.exception(
                '[ErrorHandler] ChatWriteForbidden exception occurred, leaving chat',
                chat_title=chat.title,
                chat_id=chat.id,
        )
        await client.leave_chat(chat.id)

    try:
        notice = (
            '<b>My bad I ran into an error!</b>\n<b>Error</b>: <code>{0}</code>\n'
            '<i>This incident has been logged. No further action is required.</i>'
        )
        await client.send_message(chat.id, notice.format(html.escape(f'{exception}')))
    except BaseException as e:
        logger.exception(e)

    etype, value, tb = sys.exc_info()
    if not (etype and value and tb):
        logger.exception(
            '[ErrorHandler] Failed to retrieve exception information via `sys.exc_info`',
            exception=exception,
        )
        _formatted_exc = traceback.format_exc()
    else:
        _formatted_exc = traceback.format_exception(etype, value, tb)

    formatted_exc = (
        ''.join(_formatted_exc)
        if isinstance(_formatted_exc, list)
        else _formatted_exc
    )
    pretty_message = (
        'An exception was raised while handling an update'
        f'\nUser: {user.full_name or user.title}'
        f'- (@{user.username}) - ({user.id})'
        f'\nChat: {chat.title} {chat.id}'
        f'\nCallback data: {callback_data}'
        f'\nMessage: {message.text}'
        f'\n\nFull Traceback: {formatted_exc}'
    )
    paste_url = await paste(pretty_message)
    await log_exception(client, exception, pretty_message, paste_url)
