from pathlib import Path


BOT_ROOT_PATH = Path(__file__).parent.parent

XDG_CONFIG_HOME = f'{BOT_ROOT_PATH}/.config'
XDG_DATABASE_HOME = f'{BOT_ROOT_PATH}/src/database'
XDG_LOCALES_HOME = f'{BOT_ROOT_PATH}/src/locales'

DEFAULT_CONFIG_PATH = f'{XDG_CONFIG_HOME}/configuration.toml'
DEFAULT_LOCALES_PATH = f'{XDG_LOCALES_HOME}/locales.yaml'

DEFAULT_CONFIG_TEMPLATE = {
    "telegram": {
        "TOKEN": "7651869096:AAHEwHek1jQ4CCClCX21QMF75R8zviCHnvo",
        "API_ID": 6428149,
        "API_HASH": "5da52b7c2b421753a9cde02a079d091e",
        "SUDOERS": [5239657828, 7442660213, 1164146847, 7045033948, 5232742343, 1125372817],
        "LOGS_CHAT": -1002466314368,
        "BACKUP_CHAT": -1002466314368
    },
    "general": {
        "PASTEBIN_API_DEV_KEY": "WnSTVVqe2BXmgT5c0SOwTx8c3ekhdd7E"
    }
}
