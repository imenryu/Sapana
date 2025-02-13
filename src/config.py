from pathlib import Path
from typing import Any, Self

from loguru import logger
from tomlkit import dump, loads

from . import constants
from .errors import ConfigError


class ConfigManager:
    __slots__ = ("config", "initialized")
    _instance: Self | None = None

    def __new__(cls, *args, **kwargs) -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, cfgpath: str = constants.DEFAULT_CONFIG_PATH) -> None:
        if hasattr(self, 'initialized') and self.initialized:
            return

        logger.info('Initializing configuration manager')
        logger.debug(f'Using path {cfgpath}')

        config_path = Path(cfgpath)
        self._initialize_config(config_path)

        self.config: dict[str, Any] = loads(config_path.read_text(encoding='utf-8'))
        self.initialized = True

    def _initialize_config(self, config_path: Path) -> None:
        self._create_config_directory(config_path)
        self._create_config_file(config_path)

    @staticmethod
    def _create_config_directory(config_path: Path) -> None:
        if config_path.parent.exists():
            return

        logger.info('Creating configuration directory')
        try:
            config_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise ConfigError(f'Could not create configuration directory: {e}')

    @staticmethod
    def _create_config_file(config_path: Path) -> None:
        if config_path.is_file():
            return

        logger.info('Creating configuration file')
        try:
            with config_path.open('w', encoding='utf-8') as file:
                dump(constants.DEFAULT_CONFIG_TEMPLATE, file)
        except OSError as e:
            raise ConfigError(f'Could not create configuration file: {e}')

    @classmethod
    def get(cls, section: str, option: str, fallback: str = '') -> Any:
        if not cls._instance:
            raise ConfigError('ConfigManager instance has not been initialized')

        return cls._instance.config.get(section, {}).get(option, fallback)
