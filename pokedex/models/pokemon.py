from typing import Optional, List, Dict, Any

from .resource import Resource
from . import utils


class PokemonBaseStats:
    __slots__ = ("health_points", "attack", "defense", "special_attack", "special_defense", "speed")

    def __init__(
        self,
        health_points: dict,
        attack: dict,
        defense: dict,
        special_attack: dict,
        special_defense: dict,
        speed: dict
    ) -> None:
        self.health_points = health_points
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed
        

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{stat}={getattr(self, stat)!r}' for stat in self.__slots__)})"

class PokemonSprites:
    __slots__ = ("normal", "shiny")

    def __init__(self, normal: str, shiny: str):
        self.normal = normal
        self.shiny = shiny

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{stat}={getattr(self, stat)!r}' for stat in self.__slots__)})"

class PokemonEvolveTo(Resource):
    __slots__ = ("id", "name", "min_level")

    def __init__(self, id: int, name: str, min_level: int):
        super().__init__(id=id, name=name)
        self.min_level = min_level

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{stat}={getattr(self, stat)!r}' for stat in self.__slots__)})"

class PokemonLearnableMovesByMethod(Resource):
    __slots__ = ("id", "name", "min_level", "version")

    def __init__(self, id: int, name: str, min_level: int, version: str):
        super().__init__(id=id, name=name)
        self.min_level = min_level
        self.version = version

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{stat}={getattr(self, stat)!r}' for stat in self.__slots__)})"

class PokemonLearnableMoves:
    __slots__ = ("level_up", "machine", "egg")

    def __init__(self, level_up: list[dict], machine: list[dict], egg: list[dict]):
        self.level_up = [PokemonLearnableMovesByMethod(**move) for move in level_up]
        self.machine = [PokemonLearnableMovesByMethod(**move) for move in machine]
        self.egg = [PokemonLearnableMovesByMethod(**move) for move in egg]

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{stat}={getattr(self, stat)!r}' for stat in self.__slots__)})"

class Pokemon(Resource):
    __slots__ = (
        "id", "name", "is_legendary", "is_mythical", "appear_rate", "capture_rate", "gender_rate",
        "growth_rate", "evolves_from", "evolves_to", "types", "base_stats", "ev_yields",
        "learnable_moves", "sprites", "regions"
    )

    def __init__(
        self,
        id: int,
        name: str,
        is_legendary: bool,
        is_mythical: bool,
        appear_rate: int,
        capture_rate: int,
        gender_rate: int,
        growth_rate: int,
        evolves_from: Optional[int],
        evolves_to: Optional[Dict[str, Any]],
        types: List[str],
        base_stats: Dict[str, int],
        ev_yields: Dict[str, int],
        sprites: Dict[str, str],
        regions: List[str],
        learnable_moves: List[Dict[str, Any]]
    ):
        super().__init__(id=id, name=name)
        self.is_legendary = is_legendary
        self.is_mythical = is_mythical
        self.appear_rate = appear_rate
        self.capture_rate = capture_rate
        self.gender_rate = gender_rate
        self.growth_rate = utils.get_growth_rate(growth_rate)
        self.evolves_from = evolves_from
        self.evolves_to = PokemonEvolveTo(**evolves_to) if evolves_to else None
        self.types = [utils.get_type(type) for type in types]
        self.sprites = PokemonSprites(**sprites)
        self.base_stats = PokemonBaseStats(**base_stats)
        self.ev_yields = ev_yields
        self.regions = [utils.get_region(region) for region in regions]
        self.learnable_moves = PokemonLearnableMoves(**learnable_moves)

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{stat}={getattr(self, stat)!r}' for stat in self.__slots__)})"
