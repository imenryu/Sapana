from dataclasses import dataclass
from typing import Optional, List, Dict, Any

# --------------------------
# 1. MetaResource Metaclass
# --------------------------
class MetaResource(type):
    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls, name, bases, clsdict)
        return dataclass(clsobj, init=False)

# --------------------------
# 2. Resource Class
# --------------------------
class Resource(metaclass=MetaResource):
    """A resource with a name and id"""

    id: int
    name: str

    __slots__ = ('id', 'name')

    def __init__(self, *, id: int, name: str):
        self.id = id
        self.name = name

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and other.id == self.id
            and other.name == self.name
        )

# --------------------------
# 3. Dependent Classes
# --------------------------
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

class PokemonSprites:
    __slots__ = ("normal", "shiny")

    def __init__(self, normal: str, shiny: str):
        self.normal = normal
        self.shiny = shiny

class PokemonEvolveTo(Resource):
    __slots__ = ("min_level",)

    def __init__(self, *, id: int, name: str, min_level: int):
        super().__init__(id=id, name=name)
        self.min_level = min_level

class PokemonLearnableMovesByMethod(Resource):
    __slots__ = ("min_level", "version")

    def __init__(self, *, id: int, name: str, min_level: int, version: str):
        super().__init__(id=id, name=name)
        self.min_level = min_level
        self.version = version

class PokemonLearnableMoves:
    __slots__ = ("level_up", "machine", "egg")

    def __init__(self, level_up: list[dict], machine: list[dict], egg: list[dict]):
        self.level_up = [PokemonLearnableMovesByMethod(**move) for move in level_up]
        self.machine = [PokemonLearnableMovesByMethod(**move) for move in machine]
        self.egg = [PokemonLearnableMovesByMethod(**move) for move in egg]

# --------------------------
# 4. Pokemon Class
# --------------------------
class Pokemon(Resource):
    __slots__ = (
        "is_legendary", "is_mythical", "appear_rate", "capture_rate", "gender_rate",
        "growth_rate", "evolves_from", "evolves_to", "types", "base_stats", "ev_yields",
        "learnable_moves", "sprites", "regions"
    )

    def __init__(
        self,
        *,
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
        learnable_moves: Dict[str, List[Dict[str, Any]]]
    ):
        # Initialize Resource with id and name
        super().__init__(id=id, name=name)
        
        # Initialize other attributes
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

        # Exclude tutor moves from learnable_moves
        filtered_moves = {k: v for k, v in learnable_moves.items() if k != "tutor"}
        self.learnable_moves = PokemonLearnableMoves(**filtered_moves)

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{stat}={getattr(self, stat)!r}' for stat in self.__slots__)})"
