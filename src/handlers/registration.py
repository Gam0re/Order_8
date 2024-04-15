from aiogram import types, Router, F
import re

from aiogram.filters import  StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
import src.keyboards.default.reply as kb
import src.database.models as models

import src.states.user as user_states

registration_router = Router()


async def start_registration_name(message: types.Message, state: FSMContext):
    await message.answer('Вы у нас первый раз?\nДавайте заполним некоторые данные\nВведите свое ФИО:', reply_markup=kb.back_kb)
    await state.set_state(user_states.UserFSM.write_name)

@registration_router.message(F.text=='назад')
async def to_settings(message: types.Message):
    await message.answer('меню настроек', reply_markup=kb.settings_kb)

@registration_router.message(StateFilter(user_states.UserFSM.write_name))
async def registration_name(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await message.answer('Введите свой номер телефона в формате +7хххххххххх', reply_markup=kb.back_kb)
    await state.set_state(user_states.UserFSM.write_phone)


@registration_router.message(F.text, StateFilter(user_states.UserFSM.write_phone))
async def registration_phone(message: types.Message, state: FSMContext):
        await state.update_data(user_phone=message.text)
        user_data = await state.get_data()
        await models.insert_name_and_phone(message.from_user.id, user_data.get('user_name'),
                                           user_data.get('user_phone'))
        await state.set_state(default_state)
        await message.answer('Ваши данные успешно внесены', reply_markup=kb.settings_kb)

