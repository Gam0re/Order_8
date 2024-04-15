from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

import src.database.requests as rq
import src.keyboards.default.reply as kb
import src.states.user as user_states
from src.handlers.registration import start_registration_name
from src.database.models import update_name, update_phone

settings_router = Router()

@settings_router.message(F.text=='Назад')
@settings_router.message(F.text=='Настройки')
async def settings_setup(message: types.Message):
    await message.answer('Меню настроек', reply_markup=kb.settings_kb)


@settings_router.message(F.text=='Имя')
async def setting_name(message: types.Message, state: FSMContext):
    name = await rq.get_name(tg_id=message.from_user.id)
    if not name:
        await start_registration_name(message, state)
    else:
        await message.answer(f"Ваше ФИО: {name}\nНовое значение", reply_markup=kb.back_kb)
        await state.set_state(user_states.UserFSM.rewrite_name)

@settings_router.message(F.text=='Номер')
async def setting_phone(message: types.Message, state: FSMContext):
    phone = await rq.get_number(tg_id=message.from_user.id)
    if not phone:
        await start_registration_name(message, state)
    else:
        await message.answer(f"Ваш номер: {phone}\nНовое значение", reply_markup=kb.back_kb)
        await state.set_state(user_states.UserFSM.rewrite_phone)

@settings_router.message(StateFilter(user_states.UserFSM.rewrite_name))
async def rename(message: types.Message, state: FSMContext):
        await update_name(message.from_user.id, message.text)
        await state.set_state(default_state)
        await message.answer('Имя успешно изменено', reply_markup=kb.settings_kb)

@settings_router.message(StateFilter(user_states.UserFSM.rewrite_phone))
async def rephone(message: types.Message, state: FSMContext):
        await update_phone(message.from_user.id, message.text)
        await state.set_state(default_state)
        await message.answer('Номер успешно изменен', reply_markup=kb.settings_kb)


