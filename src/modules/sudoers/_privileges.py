from hydrogram import filters

from src.decorators import router, rate_limit
from src.filters import SudoOnly
from src.locales import Locales

VALID_ACTIONS = {'access', 'update', 'remove'}


@router.message(filters.command("sudo") & SudoOnly)
@rate_limit()
async def sudo_command(client, message) -> None:
    action = user = identifier = None

    if message.reply_to_message and len(message.command) == 2:
        action = message.command[1]
        user = message.reply_to_message.from_user
    elif len(message.command) == 3:
        action = message.command[1]
        identifier = message.command[2]
        try:
            identifier = int(identifier)
            if identifier < 0:
                text = Locales.get('general', 'invalid_user_id')
                return await message.reply(text)
        except ValueError:
            if not (identifier.startswith('@') and len(identifier) < 3):
                text = Locales.get('general', 'invalid_user_format')
                return await message.reply(text)
    else:
        text = Locales.get('sudoers', 'privileges_usage')
        return await message.reply(text)

    if action not in VALID_ACTIONS:
        text = Locales.get('sudoers', 'privileges_usage')
        return await message.reply(text)
    if identifier and not user:
        try:
            user = await client.get_users(identifier)
        except PeerIdInvalid:
            text = Locales.get('general', 'invalid_user_format')
            return await message.reply(text)
    # to do
