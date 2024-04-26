import src.database.requests as rq
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


async def get_selection_btns(param=None):
    keyboard = ReplyKeyboardBuilder()
    names = await rq.get_control_types()
    for name in names:
        keyboard.add(KeyboardButton(text=f"{name}"))
    return keyboard.adjust(len(names)).as_markup()
