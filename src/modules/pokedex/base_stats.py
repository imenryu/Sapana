from contextlib import suppress

from hydrogram import filters
from hydrogram.errors import MessageNotModified
from hydrogram.types import CallbackQuery

from pokedex import Pokedex
from src.decorators import router, rate_limit
from src.filters import IsMessageExpired
from ._utils import get_pokemon_base_stats_data, get_pokemon_ev_yields_data


@router.callback_query(filters.regex(r'^ev-yields (\d+)$') & IsMessageExpired)
@rate_limit()
async def pokemon_ev_yields_callback(client, update) -> None:
    dex_id = int(update.matches[0].group(1))
    pokemon = Pokedex.get_pokemon(dex_id)
    ev_yields = get_pokemon_ev_yields_data(pokemon)
    await update.answer(ev_yields, show_alert=True)

@router.callback_query(filters.regex(r'^pokedex base-stats (\d+) (\d+)$') & IsMessageExpired)
@rate_limit()
async def pokemon_base_stats_callback(client, update) -> None:
    user = update.from_user
    user_id = int(update.matches[0].group(1))

    if user.id != user_id:
        return await update.answer('you cannot use this.')

    dex_id = int(update.matches[0].group(2))
    pokemon = Pokedex.get_pokemon(dex_id)
    caption, reply_markup = get_pokemon_base_stats_data(user, pokemon)
    with suppress(MessageNotModified):
        await update.edit_message_caption(caption=caption, reply_markup=reply_markup)
