from aiogram_dialog import DialogManager, StartMode
from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

import src.database.requests as rq
import src.keyboards.default.selection_btns as kb
import src.states.user as user_states
import src.dialogs.Selection.selection_states as selection_states

selection_router = Router()

@selection_router.message(Command(commands='selection'))
@selection_router.message(F.text == 'Подбор')
async def selection_price(message: types.Message, state: FSMContext):
    max_price, min_price = await rq.get_max_and_min()
    await message.answer(text=f'Нaпишите цену от {min_price} до {max_price} в рублях')
    await state.set_state(user_states.UserFSM.write_price)

@selection_router.message(F.text, StateFilter(user_states.UserFSM.write_price))
async def selection_control_type(message: types.Message, state: FSMContext):
    price = float(message.text)
    if price:
        await state.update_data(user_price=price)
        await message.answer(text='Выберете тип управления компрессором', reply_markup=await kb.get_selection_btns('control_type'))
        await state.set_state(user_states.UserFSM.choosing_control_type)

    else:
        await message.answer(text=f"такой цены нет, попробуйте еще раз")

@selection_router.message(F.text, StateFilter(user_states.UserFSM.choosing_control_type))
async def selection_appointment(message: types.Message, state: FSMContext):
    control_type = message.text
    if control_type:
        await state.update_data(user_control_type=control_type)
        await message.answer(text='Выберете назначение', reply_markup=await kb.get_selection_btns('appointment'))
        await state.set_state(user_states.UserFSM.choosing_appointment_type)
    else:
        await message.answer(text='Выберете из представленного списка')

@selection_router.message(F.text, StateFilter(user_states.UserFSM.choosing_appointment_type))
async def suitable_products(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    appointment_type = message.text
    if appointment_type:
        await state.update_data(user_appointment_type=appointment_type)
        await dialog_manager.start(state=selection_states.SelectionStates.searching_products, data=await state.get_data(), mode=StartMode.RESET_STACK)
    else:
        await message.answer(text='Выберете из представленного списка')
