from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/catalog', description='Каталог'),
        BotCommand(command='/cart', description='Корзина'),
        BotCommand(command='/orders', description='Заказы'),
        BotCommand(command='/settings', description='Настройки'),
        BotCommand(command='/help', description='Справка'),
        BotCommand(command='/start', description='Главное меню'),
        BotCommand(command='/news', description='Новости'),
        BotCommand(command='/selection', description='Подбор),
    ]
    await bot.set_my_commands(main_menu_commands)
