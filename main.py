import asyncio
from src.bot import bot, dp
from src.handlers.common import router
from src.handlers.help_cmd import help_router
from src.handlers.settings import settings_router
from src.handlers.registration import registration_router
from src.handlers.catalog import catalog_router
from src.handlers.selection import selection_router
from src.keyboards.set_menu import set_main_menu
from src.database.models import async_main
from src.handlers.cart import cart_router
from src.handlers.orders import order_router
from src.dialogs.Catalog.catalog_dialogs import Catalog_lvl1
from src.dialogs.Selection.selection_dialog import selection
from src.dialogs.Cart.cart_dialogs import Cart
from aiogram_dialog import setup_dialogs
from src.handlers.payment import payment_router

async def main():
    #await async_main()
    dp.include_router(router)
    dp.include_router(help_router)
    dp.include_router(catalog_router)
    dp.include_router(cart_router)
    dp.include_router(selection_router)
    dp.include_router(settings_router)
    dp.include_router(registration_router)
    dp.include_router(order_router)
    dp.include_router(payment_router)
    dp.include_router(Catalog_lvl1)
    dp.include_router(selection)
    dp.include_router(Cart)
    setup_dialogs(dp)
    await set_main_menu(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
