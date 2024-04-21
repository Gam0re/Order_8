from aiogram import types, Router, F

from aiogram.filters import CommandStart
from aiogram.filters import Command

from aiogram_dialog import DialogManager

import src.states.dialog as dialog_states
import src.keyboards.default.reply as kb
import src.database.requests as rq

router = Router()


# команда старт
@router.message(CommandStart())
@router.message(F.text == 'Главное меню')
async def start(message: types.Message):
    await rq.set_user(message.from_user.id)
    await message.answer("Вас приветствует интернет магазин кондиционеров", reply_markup=kb.start)

@router.message(Command(commands='catalog'))
@router.message(F.text == 'Каталог')
async def catalog(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(dialog_states.dialogFSM.first_level_state)

