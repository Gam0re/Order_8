from aiogram import types, Router, F

from aiogram.filters import CommandStart

import bot_template.keyboards.default.reply as kb
import bot_template.database.requests as rq

router = Router()


# команда старт
@router.message(CommandStart())
@router.message(F.text == 'Главное меню')
async def start(message: types.Message):
    await rq.set_user(message.from_user.id)
    await message.answer("Вас приветствует интернет магазин кондиционеров", reply_markup=kb.start)
