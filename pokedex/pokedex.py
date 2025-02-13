import os
import json
import difflib
from typing import List, Dict, Optional, Any

from cachetools import cached, LRUCache

from . import constants, enums
from .errors import PokedexError
from .models import Pokemon, Move

class PokedexBase:

    __slots__ = ('data', '_tried')

    def __init__(self) -> None:
        self.data: Dict[str, List[Dict[str, Any]]] = {}
        self._tried: int = 0
        self._initialize()

    #  @cached(cache=LRUCache(maxsize=3))
    def _initialize(self) -> None:
        if self._tried > 3:
            raise PokedexError('Failed to load data files after multiple attempts.')

        self._tried += 1
        for filename in os.listdir(constants.XDG_RAWDATA_HOME):
            if filename.endswith('.json'):
                filepath = os.path.join(constants.XDG_RAWDATA_HOME, filename)
                try:
                    with open(filepath, 'r', encoding='utf8') as f:
                        content = json.load(f)
                        self.data[filename[:-5]] = content
                except (FileNotFoundError, IOError, OSError) as e:
                    logger.exception(f'Error opening or reading pokedex rawdata file: {filepath}')

    #  @cached(cache=LRUCache(maxsize=100))
    def _filter(self, region: str | enums.Region) -> Optional[List[Pokemon]]:
      try:
          results: List[Pokemon] = []
          if isinstance(region, enums.Region):
              region = region.value
          for pokemon in self.data['pokemon']:
              if region in pokemon['region']:
                poke = self.get_pokemon(pokemon['id'])
                if poke:
                  results.append(poke)
          return results if results else None
      except KeyError:
          return None

    #  @cached(cache=LRUCache(maxsize=100))
    def _find_similar(self, name: str, possibilities: List[str], data_type: enums.DataType, model_class: Pokemon | Move) -> Optional[List[Pokemon | Move]]:
        results: List[Pokemon | Move] = []
        matches = difflib.get_close_matches(word=name, possibilities=possibilities)
        if matches:
            for match in matches:
                item = self._get_item(match, data_type, model_class)
                if item:
                    results.append(item)
        return results if results else None

    def get_all_pokemon(self, data_type: enums.DataType = enums.DataType.POKEMON) -> List[Pokemon]:
        return [self.get_pokemon(pokemon['id']) for pokemon in self.data[data_type.value]]

    def get_all_moves(self, data_type: enums.DataType = enums.DataType.MOVES) -> List[Move]:
        return [self.get_move(move['id']) for move in self.data[data_type.value]]

    def get_pokemon(self, id_or_name: int | str) -> Optional[Pokemon | List[Pokemon]]:
        return self._get_item(id_or_name, enums.DataType.POKEMON, Pokemon)

    def get_move(self, id_or_name: int | str) -> Optional[Move | List[Move]]:
        return self._get_item(id_or_name, enums.DataType.MOVES, Move)

    #  @cached(cache=LRUCache(maxsize=100))
    def _get_item(self, id_or_name: int | str, data_type: enums.DataType, model_class: Pokemon | Move) -> Optional[Pokemon | Move | List[Pokemon | Move]]:
        try:
            data: List[Dict[str, Any]] = self.data[data_type.value]
        except KeyError:
            self._initialize()
            return self._get_item(id_or_name, data_type, model_class)

        if isinstance(id_or_name, int):
            for item in data:
                if item['id'] == id_or_name:
                    return model_class(**item)
        elif isinstance(id_or_name, str):
            if id_or_name.isdigit():
                for item in data:
                    if item['id'] == int(id_or_name):
                        return model_class(**item)
            else:
                name = id_or_name.strip().lower().replace(' ', '-')
                for item in data:
                    if item['name'] == name:
                        return model_class(**item)
                return self._find_similar(
                    name=name,
                    possibilities=[
                        item['name']
                        for item in data
                    ],
                    data_type=data_type,
                    model_class=model_class
                )
        else:
            raise TypeError('`id_or_name` must be `int` or `str`')
