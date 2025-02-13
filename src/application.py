from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from hydrogram import Client
from hydrogram.enums import ParseMode
from hydrogram.raw.all import layer
from loguru import logger

from . import PROJECT_NAME, __version__
from .config import ConfigManager

if TYPE_CHECKING:
    from hydrogram.types import User


@dataclass(frozen=True, slots=True)
class AppParameters:
    api_id: str
    api_hash: str
    bot_token: str
    ipv6: bool
    workdir: str
    name: str = PROJECT_NAME


class Application(Client):
    __slots__ = ("me", "parameters")

    def __init__(self, parameters: AppParameters):
        super().__init__(
            name=parameters.name,
            api_id=parameters.api_id,
            api_hash=parameters.api_hash,
            bot_token=parameters.bot_token,
            ipv6=parameters.ipv6,
            workdir=parameters.workdir,
            parse_mode=ParseMode.HTML,
            sleep_threshold=60,
            max_concurrent_transmissions=2,
        )

        self.parameters = parameters
        self.me: Optional[User] = None

    async def start(self) -> None:
        await super().start()
        
        from .modules.core import ModuleLoader
        loader = ModuleLoader()
        await loader.load_all(self)

        self.me = await self.get_me()

        logger.info(
            f'{PROJECT_NAME} {__version__} running with {self.app_version} '
            f'(Layer {layer}) started on @{self.me.username}. Hi!'
        )

    async def stop(self) -> None:
        await super().stop()
        logger.info(f'{PROJECT_NAME} stopped.')
