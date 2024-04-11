from aiogram import types, Router, F

from aiogram.filters import CommandStart

import bot_template.keyboards.reply as kb

router = Router()


# команда старт
@router.message(CommandStart())
@router.message(F.text == 'Главное меню')
async def start(message: types.Message):
    await message.answer("Вас приветствует интернет магазин кондиционеров", reply_markup=kb.start)
