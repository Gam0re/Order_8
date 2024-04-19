from aiogram import types, Router, F

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

import src.keyboards.default.reply as kb
import src.database.requests as rq

router = Router()


# команда старт
@router.message(CommandStart())
@router.message(F.text == 'Главное меню')
async def start(message: types.Message, state: FSMContext):
    await rq.set_user(message.from_user.id)
    await message.answer("Вас приветствует интернет магазин кондиционеров", reply_markup=kb.start)
    await state.set_state(default_state)
