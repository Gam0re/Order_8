import asyncio
from bot import bot, dp
from src.handlers.common import router
from src.handlers.help_cmd import help_router
from src.handlers.settings import settings_router
from src.handlers.registration import registration_router
from src.handlers.catalog import catalog_router
from src.keyboards.set_menu import set_main_menu
from src.database.models import async_main


async def main():
    await async_main()
    dp.include_router(router)
    dp.include_router(help_router)
    dp.include_router(settings_router)
    dp.include_router(registration_router)
    dp.include_router(catalog_router)
    await set_main_menu(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
