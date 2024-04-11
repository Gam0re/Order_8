import asyncio
from bot_template.data.config import BOT_TOKEN

from aiogram import Bot, Dispatcher

from bot_template.handlers.common import router
from bot_template.handlers.help_cmd import help_router


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(help_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
