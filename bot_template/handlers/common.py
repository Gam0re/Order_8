from aiogram import types, Router

from aiogram.filters import CommandStart

import bot_template.keyboards.reply as kb

router = Router()

#команда старт
@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Вас приветствует интернет магазин кондиционеров", reply_markup=kb.start)
