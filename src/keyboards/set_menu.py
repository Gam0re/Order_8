from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/catalog', description='Каталог'),
        BotCommand(command='/cart', description='Корзина'),
        BotCommand(command='/history', description='История заказов'),
        BotCommand(command='/settings', description='Настройки'),
        BotCommand(command='/help', description='Справка'),
        BotCommand(command='/start', description='Главное меню'),
        BotCommand(command='/delivery', description='Информация о доставке'),
        BotCommand(command='/news', description='Новости'),
    ]
    await bot.set_my_commands(main_menu_commands)