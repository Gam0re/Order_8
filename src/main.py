import asyncio
from src.data.config import BOT_TOKEN

from aiogram import Bot, Dispatcher

from src.handlers.common import router
from src.handlers.help_cmd import help_router
from src.keyboards.set_menu import set_main_menu
from src.database.models import async_main
from src.handlers.catalog import catalog_router
from src.dialogs.Catalog.catalog_dialogs import Catalog_lvl1
from aiogram_dialog import setup_dialogs
from aiogram.fsm.storage.memory import MemoryStorage

async def main():
    await async_main()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(help_router)
    dp.include_router(catalog_router)
    dp.include_router(Catalog_lvl1)
    setup_dialogs(dp)
    await set_main_menu(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
