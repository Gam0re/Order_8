from aiogram import types, Router, F

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from src.keyboards.inline.order_registration_kb import continuing_order_registration
import src.keyboards.default.reply as kb

import src.database.requests as rq
import src.states.user as user_states

registration_router = Router()


async def start_registration_name(message: types.Message, state: FSMContext):
    await message.answer('Вы у нас первый раз?\nДавайте заполним некоторые данные\nВведите свое ФИО:')
    await state.set_state(user_states.UserFSM.write_name)


@registration_router.message(StateFilter(user_states.UserFSM.write_name))
async def registration_name(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await message.answer('Введите свой номер телефона в формате +7хххххххххх')
    await state.set_state(user_states.UserFSM.write_phone)


@registration_router.message(F.text, StateFilter(user_states.UserFSM.write_phone))
async def registration_phone(message: types.Message, state: FSMContext):
    await state.update_data(user_phone=message.text)
    user_data = await state.get_data()
    await rq.update_name_and_phone(message.from_user.id, name=user_data.get('user_name'),
                                   phone=user_data.get('user_phone'))
    if not user_data.get('from_settings_registration'):
        await message.answer(f"Ваши данные успешно внесены\nВы ввели:\nФИО: {user_data.get('user_name')}\nНомер телефона: {user_data.get('user_phone')}\nВы можете поменять свои данные в любой момент в настройках",
                             reply_markup=continuing_order_registration)
        await state.set_state(default_state)
    else:
        await message.answer('Ваши данные успешно внесены', reply_markup=kb.settings_kb)
        await state.set_state(user_states.UserFSM.settings_menu)
