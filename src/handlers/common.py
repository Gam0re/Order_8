from aiogram import types, Router, F

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from aiogram_dialog import DialogManager

import src.database.requests as rq
import src.keyboards.default.reply as kb

router = Router()


# команда старт
@router.message(CommandStart())
@router.message(F.data == 'to_main')
@router.message(F.text == 'Главное меню')
async def start(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await rq.set_user(message.from_user.id)
    await message.answer(f'Вас приветствует интернет магазин кондиционеров "Центр климата"', reply_markup=kb.start)
    await state.set_state(default_state)

