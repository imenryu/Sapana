import asyncio
import html
import sys
import traceback
from typing import Any

import aiofiles
from hydrogram import filters
from hydrogram.enums import ChatAction
from meval import meval

from src.decorators import router, rate_limit
from src.filters import SudoOnly
from src.utils.chat_action import ChatActionSender
from src.utils.utility import delete_if_exists

def _namespaces(client, message) -> dict:
    return {
        "client": client,
        "message": message,
        "reply": message.reply_to_message,
        "user": message.from_user,
        "chat": message.chat
    }

def _cleanup_code(code: str) -> str:
    if code.startswith('```') and code.endswith('```'):
        return '\n'.join(code.split('\n')[1:-1])
    return code.strip('` \n')

async def _evaluate_expression(expression: str, namespaces: dict) -> Any:
    """Evaluates a Python code in a separate thread."""
    task = asyncio.create_task(meval(expression, globals(), **locals(), **namespaces))
    return await task

async def _handle_output(client, message, output: Any, code: str) -> None:
    """Handles the output of the evaluated expression."""
    if output is None:
        await message.reply('No output.')
        return

    output_str = str(output)
    filename = 'evaluate.txt'
    try:
        # async with ChatActionSender(
        #    client=client, chat_id=message.chat.id,
        #    action=ChatAction.UPLOAD_DOCUMENT
        # ):
        async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
                await f.write(output_str)
        await message.reply_document(
                document=filename,
                caption=f'<code>{html.escape(code)}</code>'
        )
    finally:
        delete_if_exists(filename)

@router.message(filters.command("eval") & SudoOnly)
@rate_limit()
async def eval_command(client, message) -> None:
    """Evaluates a Python expression sent by a sudo user."""

    if len(message.command) < 2:
        await message.reply('No expression provided.')
        return

    namespaces = _namespaces(client, message)
    code = _cleanup_code(message.text.split(maxsplit=1)[-1])

    # async with ChatActionSender(
    #    client=client, chat_id=message.chat.id,
    #    action=ChatAction.TYPING
    # ):
    try:
            output = await _evaluate_expression(code, namespaces)
    except Exception as e:
            etype, value, tb = sys.exc_info()
            if not (etype and value and tb):
                _formatted_exc = traceback.format_exc()
            else:
                _formatted_exc = traceback.format_exception(etype, value, tb)

            formatted_exc = (
                ''.join(_formatted_exc)
                if isinstance(_formatted_exc, list)
                else _formatted_exc
            )
            output = f'{e}\n\n{formatted_exc}'

    await _handle_output(client, message, output, code)
