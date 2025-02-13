from pathlib import Path
from typing import Optional, Self

from loguru import logger
from tomlkit import loads

from src import constants
from src.errors import LocalesError


class Locales:
    __slots__ = ("locales", "initialized")
    _instance: Optional[Self] = None

    def __new__(cls, *args, **kwargs) -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, loclpath: str = constants.DEFAULT_LOCALES_PATH) -> None:
        if hasattr(self, 'initialized') and self.initialized:
            return

        logger.info('Initializing locales manager ...')
        logger.debug(f'Using path {loclpath}')

        locales_path = Path(loclpath)

        self.locales: dict[str, Any] = loads(locales_path.read_text(encoding='utf-8'))
        self.initialized = True

    @classmethod
    def get(cls, section: str, option: str, fallback: str = '') -> str:
        if not cls._instance:
            raise LocalesError('Locales instance has not been initialized')

        return cls._instance.locales.get(section, {}).get(option, fallback)
