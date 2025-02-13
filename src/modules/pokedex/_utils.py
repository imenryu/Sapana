from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from loguru import logger

from pokedex import Pokedex
from src.locales import Locales
from src.utils.keyboard import Keyboard

if TYPE_CHECKING:
    from hydrogram.types import User

    from pokedex.models.pokemon import Pokemon, PokemonLearnableMove

MOVES_PER_PAGE = 5


def get_pokemon_base_stats_data(user: User, pokemon: Pokemon) -> str:
    caption = Locales.get('pokedex', 'pokemon_basestats')
    keyboard = [[("Back to Pokemon", f"pokedex about {user.id} {pokemon.id}")]]
    return caption.format(pokemon.base_stats), Keyboard(keyboard)

def get_pokemon_ev_yields_data(pokemon: Pokemon) -> str:
    caption, evs = Locales.get('pokedex', 'pokemon_ev_yields'), ''
    for stat, ev_yield in pokemon.ev_yields.items():
        evs += f'\n\n+{ev_yield} {stat}'
    return caption.format(name=pokemon.name.capitalize(), evs=evs)

def get_pokemon_reply_markup(user: User, pokemon: Pokemon):
    keyboard: list[list[tuple[str, str]]] = []

    evolution_buttons: list[tuple[str, str]] = []
    if pokemon.evolves_from:
        try:
            evolves_from = Pokedex.get_pokemon(pokemon.evolves_from)
            evolution_buttons.append((evolves_from.name.capitalize(), f'pokedex about {user.id} {evolves_from.id}'))
        except Exception:
            logger.exception(f'Error fetching evolution data for: {pokemon.name}')
    if pokemon.evolves_to:
        try:
            evolves_to = Pokedex.get_pokemon(pokemon.evolves_to.id)
            evolution_buttons.append((f'{evolves_to.name.capitalize()} (min lvl {pokemon.evolves_to.min_level})', f'pokedex about {user.id} {evolves_to.id}'))
        except Exception:
            logger.exception(f'Error fetching evolution data for: {pokemon.name}')

    if evolution_buttons:
        keyboard.append(evolution_buttons)

    keyboard.append([
        ('Base Stats', f'pokedex base-stats {user.id} {pokemon.id}'),
        ('EV yields', f'ev-yields {pokemon.id}')
    ])

    keyboard.append([('Learnable Moves', f'pokedex learnable-moves {user.id} {pokemon.id} level-up 0')])
    return Keyboard(keyboard)

def get_pokemon_data(user: User, pokemon: Pokemon) -> tuple:
    photo = pokemon.sprites.normal
    reply_markup = get_pokemon_reply_markup(user, pokemon)
    caption_data = {
        'id': pokemon.id,
        'name': pokemon.name.capitalize(),
        'type': ', '.join(type.value.capitalize() for type in pokemon.types),
        'growth_rate': pokemon.growth_rate.value.capitalize(),
        'region': ', '.join(region.value.capitalize() for region in pokemon.regions)
    }
    caption = Locales.get('pokedex', 'pokemon_about')
    return photo, caption.format(**caption_data), reply_markup

def get_similar_pokemon(user: User, pokemon: list[Pokemon]) -> tuple:
    keyboard: list[list[tuple[str, str]]] = []
    for poke in pokemon:
        keyboard.append([(poke.name, f'pokedex about {user.id} {poke.id}')])
    text = Locales.get('pokedex', 'similar_pokemon')
    return text, Keyboard(keyboard)

def get_pokemon_learnable_moves_reply_markup(user: User, pokemon: Pokemon, method: str, offset: int):
    keyboard: list[list[tuple[str, str]]] = []

    if method == 'level-up':
        _moves: list[PokemonLearnableMove] = pokemon.learnable_moves.level_up
    elif method == 'machine':
        _moves: list[PokemonLearnableMove] = pokemon.learnable_moves.machine
    total_moves = len(_moves)

    has_previous = offset > 0
    has_next = offset + MOVES_PER_PAGE < total_moves

    current_page = (offset // MOVES_PER_PAGE) + 1
    total_pages = (total_moves + MOVES_PER_PAGE - 1) // MOVES_PER_PAGE
    last_page = current_page == total_pages 

    level_up = machine = None

    if method == 'level-up':
        level_up = ('• Level Up •', 'ignore')
        machine = ('TM / TR', f'pokedex learnable-moves {user.id} {pokemon.id} machine 0')
    elif method == 'machine':
        level_up = ('Level Up', f'pokedex learnable-moves {user.id} {pokemon.id} level-up 0')
        machine = ('• TM / TR •', 'ignore')

    if level_up and machine:
        keyboard.append([level_up, machine])

    navigation_buttons: list[tuple[str, str]] = []
    if has_previous:
        navigation_buttons.append(("Previous", f"pokedex learnable-moves {user.id} {pokemon.id} {method} {offset - MOVES_PER_PAGE}"))
    navigation_buttons.append((f'{current_page}/{total_pages}', 'ignore'))
    if has_next and not last_page:
        navigation_buttons.append(("Next", f"pokedex learnable-moves {user.id} {pokemon.id} {method} {offset + MOVES_PER_PAGE}"))

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    keyboard.append([("Back to Pokemon", f"pokedex about {user.id} {pokemon.id}")])
    return Keyboard(keyboard)

def get_pokemon_learnable_moves_data(user: User, pokemon: Pokemon, method: str, offset: int) -> tuple:
    try:
        if method == 'level-up':
            _learnable_moves: list[PokemonLearnableMove] = pokemon.learnable_moves.level_up
        elif method == 'machine':
            _learnable_moves: list[PokemonLearnableMove] = pokemon.learnable_moves.machine
        else:
            raise ValueError('method invalid')
        learnable_moves = _learnable_moves[offset:offset + MOVES_PER_PAGE]
    except (IndexError, ValueError):
        learnable_moves = []
        logger.warning(f'Offset {offset} is out of range for {pokemon.name} learnable moves.')

    if not learnable_moves:
        return 'No more learnable moves found.', Keyboard([[("Back to Pokemon", f"pokedex about {user.id} {pokemon.id}")]])

    caption = '<b><u>Learnable Moves</u></b>\n'
    for learnable_move in learnable_moves:
        move = Pokedex.get_move(learnable_move.id)
        if not move:
            continue
        caption_data = {
            'name': f'{move.name} {move.type.value} ({move.damage_class})',
            'power': move.power,
            'accuracy': move.accuracy,
            'min_level': learnable_move.min_level
        }
        move_about = Locales.get('pokedex', 'pokemon_learnable_moves')
        caption += '\n\n' + move_about.format(**caption_data)

    reply_markup = get_pokemon_learnable_moves_reply_markup(user, pokemon, method, offset)
    return caption, reply_markup
