from .. import enums
from ..utils import RegionDict, TypeDict, MoveDamageClassDict

def get_region(region: str) -> enums.Region:
  return RegionDict.get(region)

def get_type(pokemon_type: str) -> enums.Type:
  return TypeDict.get(pokemon_type)

def get_damage_class(damage_class: str) -> enums.MoveDamageClass:
  return MoveDamageClassDict.get(damage_class)

def get_learn_method(method: str) -> enums.MoveLearnMethod:
  if method == 'level-up':
    _method = enums.MoveLearnMethod.LEVEL_UP
  elif method == 'egg':
    _method = enums.MoveLearnMethod.EGG
  elif method == 'machine':
    _method = enums.MoveLearnMethod.MACHINE
  else:
    _method = enums.MoveLearnMethod.LEVEL_UP
  return _method

def get_growth_rate(growth_rate: str) -> enums.GrowthRate:
  if growth_rate in {'slow', 'fast-then-very-slow'}:
    _growth_rate = enums.GrowthRate.SLOW 
  elif growth_rate == 'medium-slow':
    _growth_rate = enums.GrowthRate.MEDIUM_SLOW
  elif growth_rate == 'medium':
    _growth_rate = enums.GrowthRate.MEDIUM
  elif growth_rate == 'slow-then-very-fast':
    _growth_rate = enums.GrowthRate.MEDIUN_FAST
  elif growth_rate == 'fast':
    _growth_rate = enums.GrowthRate.FAST
  else:
    raise Exception(f'growth_rate not supported: {growth_rate}')
  return _growth_rate
