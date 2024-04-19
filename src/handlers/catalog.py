from aiogram import types, Router, F

from aiogram.filters import Command

from aiogram_dialog import DialogManager, StartMode

catalog_router = Router()

from src.dialogs.Catalog.states import Catalog_levels

# команда старт
@catalog_router.message(Command('catalog'))
@catalog_router.message(F.text == 'Каталог')
async def catalog_lvl1(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(Catalog_levels.level_1, mode=StartMode.RESET_STACK)
