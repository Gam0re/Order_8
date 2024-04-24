import src.database.requests as rq
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


async def get_selection_btns(param=None):
    keyboard = ReplyKeyboardBuilder()
    if param == 'control_type':
        names = await rq.get_control_types()
    elif param == 'appointment':
        names = await rq.get_appointment_types()
    for name in names:
        keyboard.add(KeyboardButton(text=f"{name}"))
    return keyboard.adjust(len(names)).as_markup()