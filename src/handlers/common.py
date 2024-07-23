from aiogram import types, Router, F

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

import src.keyboards.default.reply as kb
import src.database.requests as rq

router = Router()

common_config = ... #тут подгрузить bot_config.json["texts"]["common"]

# команда старт
@router.message(CommandStart())
@router.message(F.data == 'to_main')
@router.message(F.text == common_config['reply_button'])
async def start(message: types.Message, state: FSMContext):
    await rq.set_user(message.from_user.id)
    await message.answer(common_config['start_text'], reply_markup=kb.start)
    await state.set_state(default_state)
