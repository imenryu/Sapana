from enum import Enum


class DataType(Enum):
    POKEMON = 'pokemon'
    MOVES = 'moves'

class Region(Enum):
  KANTO = 'kanto'
  JOHTO = 'johto'
  HOENN = 'hoenn'
  SINNOH = 'sinnoh'
  UNOVA = 'unova'
  KALOS =  'kalos'
  ALOLA = 'alola'
  GALAR = 'galar'
  HISUI = 'hisui'
  PALDEA = 'paldea'

class Type(Enum):
  NORMAL = 'normal'
  FIGHTING = 'fighting'
  FLYING = 'flying'
  POISON = 'poison'
  GROUND = 'ground'
  ROCK = 'rock'
  BUG = 'bug'
  GHOST = 'ghost'
  STEEL = 'steel'
  FIRE = 'fire'
  WATER = 'water'
  GRASS = 'grass'
  ELECTRIC = 'electric'
  PSYCHIC = 'psychic'
  ICE = 'ice'
  DRAGON = 'dragon'
  DARK = 'dark'
  FAIRY = 'fairy'
  STELLAR = 'stellar'
  UNKNOWN = 'unknown'
  SHADOW = 'shadow'

class Nature(Enum):
  HARDY = 'hardy'
  BOLD = 'bold'
  MODEST = 'modest'
  CALM = 'calm'
  TIMID = 'timid'
  LONELY = 'lonely'
  DOCILE = 'docile'
  MILD = 'mild'
  GENTLE = 'gentle'
  HASTY = 'hasty'
  ADAMANT = 'adamant'
  IMPISH = 'impish'
  BASHFUL = 'bashful'
  CAREFUL = 'careful'
  RASH = 'rash'
  JOLLY = 'jolly'
  NAUGHTY = 'naughty'
  LAX = 'lax'
  QUIRKY = 'quirky'
  NAIVE = 'naive'
  BRAVE = 'brave'
  RELAXED = 'relaxed'
  QUIET = 'quiet'
  SASSY = 'sassy'
  SERIOUS = 'serious'

class GrowthRate(Enum):
  SLOW = 'slow'
  MEDIUM_SLOW = 'medium-slow'
  MEDIUM = 'medium'
  MEDIUM_FAST = 'medium-fast'
  FAST = 'fast'

class Gender(Enum):
  MALE = 'male'
  FEMALE = 'female'
  GENDERLESS = 'genderless'

class MoveLearnMethod(Enum):
  LEVEL_UP = 'level-up'
  TUTOR = 'tutor'
  MACHINE = 'machine'
  EGG = 'egg'
  FORM_CHANGE = 'form-change'

class MoveDamageClass(Enum):
  PHYSICAL = 'physical'
  SPECIAL = 'special'
