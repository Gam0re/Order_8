import asyncio

from aiogram import Bot, Dispatcher

from bot_template.handlers.common import router

async def main():
    bot = Bot(token="6626161631:AAH9Nro2O1J2SYb8mIUsX67WG2QviCDyAS4")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
