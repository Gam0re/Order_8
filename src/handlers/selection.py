from aiogram_dialog import DialogManager, StartMode
from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from aiogram.fsm.state import default_state

import re

import src.keyboards.default.reply as kb
import src.database.requests as rq
import src.states.user as user_states
import src.dialogs.Selection.selection_states as selection_states

selection_router = Router()

pattern = '\s{0,}?\d+[,.]?\d{0,}?\s{0,}?\D{0,}?'

@selection_router.message(Command(commands='selection'))
@selection_router.message(F.text == 'Подбор')
async def selection_control_type(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
        await dialog_manager.done()
        await message.answer(text='Выберете тип управления компрессором', reply_markup=kb.type_comp_kbd)
        await state.set_state(user_states.UserFSM.choosing_control_type)


@selection_router.message(F.text, StateFilter(user_states.UserFSM.choosing_control_type))
async def selection_control_type(message: types.Message, state: FSMContext):
    type_comp = message.text
    if type_comp:
        await state.update_data(user_type_comp=type_comp)
        min_price = await rq.get_min(await state.get_data())
        await state.update_data(min_price=min_price)
        await message.answer(text=f'Нaпишите стоимость начиная от {min_price} в рублях (напишите только число)')
        await state.set_state(user_states.UserFSM.write_price)

@selection_router.message(F.text, StateFilter(user_states.UserFSM.write_price))
async def suitable_products(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    price = float(message.text)
    if price:
        min_price = await state.get_data()
        if price < min_price['min_price']:
            await message.answer(text='Вы ввели сумму меньше мимнимальной, попробуйте еще раз')
        else:
            await state.update_data(user_price = price)
            await state.update_data(user_id = message.from_user.id)
            await dialog_manager.start(state=selection_states.SelectionStates.searching_products, data=await state.get_data(), mode=StartMode.RESET_STACK)
            await state.set_state(default_state)
    else:
        await message.answer(text='Ввод некорректен, повторите пожалуйста')
