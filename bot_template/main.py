import asyncio
from environs import Env

from aiogram import Bot, Dispatcher

from bot_template.handlers.common import router
from bot_template.handlers.help_cmd import help_router


async def main():
    env = Env()
    env.read_env()
    bot = Bot(token=env('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(help_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
