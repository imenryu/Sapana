from . import enums

MAX_IV_PER_STAT = 31
MAX_EV_PER_STAT = 252

STATS_TEMPLATE = [
    'health_points',
    'attack',
    'defence',
    'special_attack',
    'special_defence',
    'speed'
]

RegionDict = {
  'kanto': enums.Region.KANTO,
  'johto': enums.Region.JOHTO,
  'hoenn': enums.Region.HOENN,
  'sinnoh': enums.Region.SINNOH,
  'unova': enums.Region.UNOVA,
  'kalos': enums.Region.KALOS,
  'alola': enums.Region.ALOLA,
  'galar': enums.Region.GALAR,
  'hisui': enums.Region.HISUI,
  'paldea': enums.Region.PALDEA
}

TypeDict = {
    "normal": enums.Type.NORMAL,
    "fighting": enums.Type.FIGHTING,
    "flying": enums.Type.FLYING,
    "poison": enums.Type.POISON,
    "ground": enums.Type.GROUND,
    "rock": enums.Type.ROCK,
    "bug": enums.Type.BUG,
    "ghost": enums.Type.GHOST,
    "steel": enums.Type.STEEL,
    "fire": enums.Type.FIRE,
    "water": enums.Type.WATER,
    "grass": enums.Type.GRASS,
    "electric": enums.Type.ELECTRIC,
    "psychic": enums.Type.PSYCHIC,
    "ice": enums.Type.ICE,
    "dragon": enums.Type.DRAGON,
    "dark": enums.Type.DARK,
    "fairy": enums.Type.FAIRY,
    "stellar": enums.Type.STELLAR,
    "unknown": enums.Type.UNKNOWN,
    "shadow": enums.Type.SHADOW
}

MoveDamageClassDict = {
    'physical': enums.MoveDamageClass.PHYSICAL,
    'special': enums.MoveDamageClass.SPECIAL
}
