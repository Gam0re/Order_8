from aiogram import types, Router, F

from aiogram.filters import Command

import src.keyboards.inline.catalog as cl

catalog_router = Router()


# команда старт
@catalog_router.message(Command('catalog'))
@catalog_router.message(F.text == 'Каталог')
async def catalog(message: types.Message):
    await message.answer('Выберете категорию товара', reply_markup=await cl.catalog_level_1())
