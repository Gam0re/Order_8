from aiogram.types import BotCommand
from src.handlers.common import router
from src.handlers.help_cmd import help_router
from src.handlers.settings import settings_router
from src.handlers.registration import registration_router
from src.handlers.catalog import catalog_router
from src.handlers.selection import selection_router
from src.handlers.cart import cart_router
from src.handlers.orders import order_router
from src.dialogs.Catalog.catalog_dialogs import Catalog_lvl1
from src.dialogs.Selection.selection_dialog import selection
from src.handlers.payment import payment_router


routers_table = {
    "router": router,
    "help_router": help_router,
    "catalog_router": catalog_router,
    "Catalog_lvl1": Catalog_lvl1,
    "selection": selection,
    "cart_router": cart_router,
    "selection_router": selection_router,
    "settings_router": settings_router,
    "registration_router": registration_router,
    "order_router": order_router,
    "payment_router": payment_router
}

def names_2_routers(routers_list: list):
    return [routers_table[router_name] for router_name in routers_list]

def gen_commands_list(commands_list: list):
    return [BotCommand() ]