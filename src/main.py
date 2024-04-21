import asyncio

from src.data.config import BOT_TOKEN

from aiogram_dialog import Dialog, Window

from aiogram import Bot, Dispatcher

from src.handlers.common import router
from src.handlers.help_cmd import help_router
from src.handlers.settings import settings_router
from src.handlers.registration import registration_router
from src.keyboards.set_menu import set_main_menu
#from src.database.models import async_main
from src.handlers.catalog import catalog_router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from src.dialogs_windows.Dialog_ import bot_catalog_dialogs



async def main():
    #await async_main()
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    dp.include_router(help_router)
    dp.include_router(settings_router)
    dp.include_router(registration_router)
    dp.include_router(catalog_router)
    dialogs = await bot_catalog_dialogs()
    for dialog in dialogs:
        dp.include_router(dialog)
    setup_dialogs(dp)
    await set_main_menu(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
