from contextlib import suppress

from hydrogram import filters
from hydrogram.errors import MessageNotModified
from hydrogram.types import CallbackQuery, InputMediaPhoto

from pokedex import Pokedex 
from src.decorators import router, rate_limit
from src.filters import IsMessageExpired, SudoOnly
from ._utils import get_pokemon_data, get_similar_pokemon

@router.message(filters.command('pokedex') & SudoOnly)
@rate_limit()
async def pokedex_command(client, message) -> None:
    if len(message.command) < 2:
        await message.reply('No expression provided.')
        return

    id_or_name = message.text.split(maxsplit=1)[1]

    try:
        id_or_name = int(id_or_name)
    except ValueError:
        pass

    pokemon = Pokedex.get_pokemon(id_or_name)
    if pokemon is None:
        await message.reply('something went wrong')
    elif isinstance(pokemon, list):
        text, reply_markup = get_similar_pokemon(message.from_user, pokemon)
        await message.reply(text=text, reply_markup=reply_markup)
    else:
        photo, caption, reply_markup = get_pokemon_data(message.from_user, pokemon)
        await message.reply_photo(photo=photo, caption=caption, reply_markup=reply_markup)


@router.callback_query(filters.regex(r'^pokedex about (\d+) (\d+)$') & IsMessageExpired)
@rate_limit()
async def pokedex_callback(client, update) -> None:
    user = update.from_user
    user_id = int(update.matches[0].group(1))

    if user.id != user_id:
        return await update.answer('you cannot use this.')

    dex_id = int(update.matches[0].group(2))
    pokemon = Pokedex.get_pokemon(dex_id)

    photo, caption, reply_markup = get_pokemon_data(user, pokemon)
    with suppress(MessageNotModified):
        await update.edit_message_media(InputMediaPhoto(media=photo, caption=caption), reply_markup=reply_markup)
