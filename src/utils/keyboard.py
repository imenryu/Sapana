from typing import List, Tuple, Optional
from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def Keyboard(
  rows: Optional[List[List[Tuple[str, str]]]] = None
) -> InlineKeyboardMarkup:
    if rows is None:
        rows = []

    lines = []
    for row in rows:
        line = []
        for button in row:
            button = (
                btn(button, button)
                if isinstance(button, str)
                else btn(*button)
            )
            line.append(button)
        lines.append(line)
    return InlineKeyboardMarkup(inline_keyboard=lines)


def btn(
  text: str, value: str,
  type: str = "callback_data"
) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, **{type: value})
