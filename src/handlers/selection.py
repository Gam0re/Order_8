from aiogram_dialog import DialogManager, StartMode
from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from aiogram.fsm.state import default_state

import src.database.requests as rq
import src.keyboards.default.selection_btns as kb
import src.states.user as user_states
import src.dialogs.Selection.selection_states as selection_states

selection_router = Router()

@selection_router.message(Command(commands='selection'))
@selection_router.message(F.text == 'Подбор')
async def selection_price(message: types.Message, state: FSMContext):
    max_price, min_price = await rq.get_max_and_min()
    await message.answer(text=f'Нaпишите максимальную стоимость до {max_price} в рублях')
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
async def selection_square(message: types.Message, state: FSMContext):
    control_type = message.text
    if control_type:
        await state.update_data(user_control_type=control_type)
        await message.answer(text='На какую площадь рассчитан кондиционер?')
        await state.set_state(user_states.UserFSM.choosing_square)
    else:
        await message.answer(text='Выберете из представленного списка')

@selection_router.message(F.text, StateFilter(user_states.UserFSM.choosing_square))
async def selection_power(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    square = message.text
    if square:
        await state.update_data(user_square=square)
        await message.answer(text='Укажите мощность в кВт')
        await state.set_state(user_states.UserFSM.choosing_power)
    else:
        await message.answer(text='Выберете из представленного списка')

@selection_router.message(F.text, StateFilter(user_states.UserFSM.choosing_power))
async def suitable_products(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    power = message.text
    if power:
        await state.update_data(user_power=power)
        await dialog_manager.start(state=selection_states.SelectionStates.searching_products, data=await state.get_data(), mode=StartMode.RESET_STACK)
        await state.set_state(default_state)
    else:
        await message.answer(text='Выберете из представленного списка')
