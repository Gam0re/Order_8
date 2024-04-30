from aiogram import types, Router, F

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from aiogram_dialog import DialogManager

import src.keyboards.default.reply as kb
from src.keyboards.inline.select_opt import opt_kb
import src.database.requests as rq

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
    if await rq.get_opt(message.from_user.id) is None:
        await message.answer(
            'Вас приветствует интернет магазин кондиционеров "Центр климата", для начала выберите подходящуюю для вас категорию'
            '', reply_markup=opt_kb)
    else:
        await message.answer(f'Вас приветствует интернет магазин кондиционеров "Центр климата"',
                             reply_markup=kb.start)
    await state.set_state(default_state)


@router.callback_query(F.data == 'opt')
async def get_opt(callback: types.CallbackQuery):
    await rq.set_user(callback.from_user.id, True)
    await callback.message.answer(f'Отлично! Рады вас приветствовать {callback.from_user.first_name}.\nВыберете, что хотите сделать', reply_markup=kb.start)

@router.callback_query(F.data == 'user')
async def get_user(callback: types.CallbackQuery):
    await rq.set_user(callback.from_user.id, False)
    await callback.message.answer(f'Отлично! Рады вас приветствовать {callback.from_user.first_name}.\nВыберете, что хотите сделать', reply_markup=kb.start)
