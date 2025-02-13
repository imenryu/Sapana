from __future__ import annotations

import inspect
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING

from hydrogram.handlers.handler import Handler
from loguru import logger

if TYPE_CHECKING:
    from types import ModuleType
    
    from hydrogram import Client


class ModuleLoader:
    """Discovers, loads, and registers modules and their handlers."""

    def __init__(self) -> None:
        """Initializes the ModuleLoader."""
        self.modules: dict[str, dict[str, list[str]]] = {}
        self.parent_path: Path = Path(__file__).parent
        self.loaded_modules: set[str] = set()

    async def discover_modules(self) -> None:
        """Discovers modules (directories containing Python files) in the parent directory."""
        logger.debug('Discovering modules...')

        for entry in self.parent_path.iterdir():
            if entry.is_dir() and entry.exists():
                module_name = entry.name
                handlers = [
                    f"{module_name}.{file.stem}"
                    for file in entry.glob("*.py")
                    if not file.name.startswith("_")
                ]
                if handlers:
                    self.modules[module_name] = {"handlers": handlers}
                    logger.debug(f'Discovered module: {module_name} with handlers: {handlers}')
                else:
                    logger.warning(f'Module `{module_name}` has no handlers. Skipping.')

    async def load_module(self, client: Client, module_name: str, handlers: list[str]) -> bool:
        """Loads a specific module and registers its handlers.

        Args:
            client: The Hydrogram client instance.
            module_name: The name of the module to load.
            handlers: A list of handler names within the module.

        Returns:
            True if the module was loaded successfully, False otherwise.
        """
        if module_name in self.loaded_modules:
            logger.warning(f'Module `{module_name}` already loaded. Skipping.')
            return True

        logger.debug(f'Loading module: {module_name}')
        success = True

        for handler_path in handlers:
            try:
                component: ModuleType = import_module(f".{handler_path}", "src.modules")
                logger.debug(f'Imported component: {component.__name__}')

                for name, obj in vars(component).items():
                    if not (inspect.isfunction(obj) and hasattr(obj, "handlers")):
                        continue

                    for handler_data in obj.handlers:
                        handler: Handler = handler_data.get("handler")
                        group: int = handler_data.get("group", 0)

                        if not isinstance(handler, Handler):
                            logger.warning(f'Invalid handler type: {type(handler).__name__} in {module_name}.{name}. Skipping handler.')
                            continue

                        client.add_handler(handler, group)
                        logger.debug(f'Handler registered successfully: {handler} from {module_name}.{name}')

            except (ModuleNotFoundError, AttributeError, TypeError) as e:
                logger.exception(f'Error loading handler: {handler_path}')
                success = False
                continue

        if success:
            self.loaded_modules.add(module_name)
            logger.debug(f'Module loaded successfully: {module_name}')
            return True
        else:
            logger.warning(f'Module `{module_name}` loaded with errors.')
            return False

    async def load_all(self, client: Client) -> None:
        """Loads all discovered modules."""
        logger.debug('Loading all modules...')

        await self.discover_modules()

        loaded_count = 0
        for module_name, module_info in self.modules.items():
            if await self.load_module(client, module_name, module_info["handlers"]):
                loaded_count += 1

        logger.info(f'Loaded {loaded_count} of {len(self.modules)} modules')
        if self.modules:
            logger.info(f'Loaded modules: {self.loaded_modules}')
        else:
            logger.info('No modules found to load.')
