from .resource import Resource
from . import utils

class Move(Resource):
    __slots__ = ("id", "name", "power", "accuracy", "type", "damage_class")

    def __init__(
      self,
      id: int,
      name: str,
      power: int,
      accuracy: int,
      type: str,
      damage_class: str
    ) -> None:
      super().__init__(id=id, name=name)
      self.power = power
      self.accuracy = accuracy
      self.type = utils.get_type(type)
      self.damage_class = utils.get_damage_class(damage_class)

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{stat}={getattr(self, stat)!r}' for stat in self.__slots__)})"
