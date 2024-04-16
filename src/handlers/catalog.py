from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

import src.database.requests as rq
import src.keyboards.default.reply as kb
import src.states.user as user_states


catalog_router = Router()

@catalog_router.message(F.text=='Каталог')
async def catalog_start(message: types.Message):
    await message.answer('Выберете интересующую вас модель', reply_markup=kb.companys_Inkb)


@catalog_router.callback_query(lambda c: c.data and c.data.endswith('btn'))
async def model_selected(callback_query: types.CallbackQuery):
    await rq.get_models(callback_query.data[:-4])


