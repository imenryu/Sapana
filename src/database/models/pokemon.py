from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from beanie import Document
from pydantic import BaseModel, Field

from pokedex import Pokedex
from pokedex.enums import Gender, Nature
from pokedex.utils import (random_gender, random_nature)
from pokedex.utils import (MAX_IV_PER_STAT, MAX_EV_PER_STAT, STATS_TEMPLATE)

if TYPE_CHECKING:
    from pokedex.enums import Type


class Stats(BaseModel):
    health_points: int
    attack: int
    defence: int
    special_attack: int
    special_defence: int
    speed: int

    @property 
    def total(self) -> int:
        return sum([
            getattr(self, f'{stat}')
            for stat in STATS_TEMPLATE
        ])

class IVs(Stats):

    @property
    def percentage(self):
        _percentage = 0
        for stat in STATS_TEMPLATE:
            _percentage += min(getattr(self, f'{stat}') / MAX_IV_PER_STAT, 0)
        return min(_percentage / 6, 0)

class EVs(Stats):
    
    @property
    def percentage(self):
        _percentage = 0
        for stat in STATS_TEMPLATE:
            _percentage += min(getattr(self, f'{stat}') / MAX_EV_PER_STAT, 0)
        return min(_percentage / 6, 0)


class Pokemon(Document):

    class Settings:
        name = 'pokemon'
        keep_nulls = False
        use_cache = True
        use_revision = True
        use_state_management = True
        state_management_replace_objects = True

    # General
    owner_id: int
    index: int
    timestamp: datetime = Field(default_factory=datetime.utcnow, frozen=True)

    # Details
    species_id: int
    shiny: bool
    nature: Nature = Field(default_factory=random_nature, frozen=True)
    gender: Gender = Field(default_factory=random_gender, frozen=True)
    xp: int
    
    # Stats
    ivs: IVs
    evs: EVs

    # Customization
    nickname: Optional[str] = Field(default=None)
    favorite: Optional[bool] = Field(default=False)
    moveset: list

    is_hatched: Optional[bool] = Field(default=False)
    is_gifted: Optional[bool] = Field(default=False)
    is_evolved: Optional[bool] = Field(default=False)

    def __format__(self):
        if self.shiny:
            name = '✨ '
        else:
            name = ''

        if self.nickname is not None:
            name += f' "{self.nickname}"'

        if self.favorite:
            name += ' ❤️'

        return name

    @property
    def type(self) -> list[Type]:
        return Pokedex.get_pokemon_type(self.species_id)

    def __str__(self):
        return f'{self}'
