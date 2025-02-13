import asyncio

import uvloop
from hydrogram import idle
from hydrogram.errors import FloodWait
from loguru import logger

from . import constants, health_checker
from .application import AppParameters, Application
from .config import ConfigManager
from .locales import Locales


async def pre_process() -> ConfigManager:
    health_checker.check()
    config = ConfigManager()
    _ = Locales()
    return config

async def main() -> None:
    config = await pre_process()

    params = AppParameters(
        api_id=config.get("telegram", "API_ID"),
        api_hash=config.get("telegram", "API_HASH"),
        bot_token=config.get("telegram", "TOKEN"),
        ipv6=False,
        workdir=constants.BOT_ROOT_PATH.as_posix()
    )

    app = Application(params)

    try:
        await app.start()
        await idle()
    except FloodWait as fw:
        logger.exception(fw)
    except Exception:
        logger.exception("An error occurred during application's client operation")
    finally:
        try:
            await app.stop()
        except ConnectionError:
            pass


if __name__ == "__main__":
    try:
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(main())
    except KeyboardInterrupt:
        logger.warning('Forced stop... Bye!', exc_info=True)
    except Exception:
        logger.critical('Unexpected error occurred', exc_info=True)
