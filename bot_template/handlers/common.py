from aiogram import types, Router

from aiogram.filters import CommandStart

import keyboards.reply as kb
import database.requests as rq
router = Router()

#команда старт
@router.message(CommandStart())
async def start(message: types.Message):
    await rq.set_user(message.from_user.id)
    await message.answer("Вас приветствует интернет магазин кондиционеров", reply_markup=kb.start)
