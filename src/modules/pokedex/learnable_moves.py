from contextlib import suppress

from hydrogram import filters
from hydrogram.errors import MessageNotModified
from hydrogram.types import CallbackQuery

from pokedex import Pokedex
from src.decorators import router, rate_limit
from src.filters import IsMessageExpired
from ._utils import get_pokemon_learnable_moves_data


@router.callback_query(filters.regex(r'^pokedex learnable-moves (\d+) (\d+) (.+) (\d+)$') & IsMessageExpired)
@rate_limit()
async def pokemon_learnable_moves_callback(client, update) -> None:
    user = update.from_user
    user_id = int(update.matches[0].group(1))

    if user.id != user_id:
        return await update.answer('you cannot use this.')

    dex_id = int(update.matches[0].group(2))
    pokemon = Pokedex.get_pokemon(dex_id)
    method = update.matches[0].group(3)
    offset = int(update.matches[0].group(4))
    caption, reply_markup = get_pokemon_learnable_moves_data(user, pokemon, method, offset)
    with suppress(MessageNotModified):
        await update.edit_message_caption(caption=caption, reply_markup=reply_markup)
