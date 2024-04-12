import asyncio
from data.config import BOT_TOKEN

from aiogram import Bot, Dispatcher

from handlers.common import router
from handlers.help_cmd import help_router
from keyboards.set_menu import set_main_menu
from database.models import async_main


async def main():
    await async_main()
    bot = Bot(token="6626161631:AAH9Nro2O1J2SYb8mIUsX67WG2QviCDyAS4")
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(help_router)
    await set_main_menu(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
