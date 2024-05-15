from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Select
from .states import Cart_levels
from ..Catalog.states import Catalog_levels

import src.keyboards.default.reply as kb

import src.database.requests as rq
from ...keyboards.inline.order_registration_kb import yes_no_kb




async def to_main(callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,):
    await dialog_manager.done()
    await callback_query.message.answer('Вас приветствует интернет магазин кондиционеров "Центр климата"', reply_markup=kb.start)

async def selected_product(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["product_id"] = item_id
    await dialog_manager.switch_to(Cart_levels.product_card)

async def delete(callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,):
    await rq.orm_delete_from_cart(callback_query.from_user.id, int(dialog_manager.current_context().dialog_data.get('product_id')))
    if await rq.orm_get_user_carts(callback_query.from_user.id) == []:
        await dialog_manager.done()
        await callback_query.message.delete()
        await callback_query.message.answer('Корзина пуста')
    else:
        await dialog_manager.switch_to(Cart_levels.select_products)

async def reduce(callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,):
    prod_del = await rq.orm_reduce_product_in_cart(callback_query.from_user.id, int(dialog_manager.current_context().dialog_data.get('product_id')))
    if not prod_del:
        print(rq.orm_get_user_carts(callback_query.from_user.id))
        if await rq.orm_get_user_carts(callback_query.from_user.id) == []:
            await dialog_manager.done()
            await callback_query.message.delete()
            await callback_query.message.answer('Корзина пуста')
        else:
            await dialog_manager.switch_to(Cart_levels.select_products)

async def increase(callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,):
    await rq.orm_add_to_cart(callback_query.from_user.id, int(dialog_manager.current_context().dialog_data.get('product_id')))

async def to_catalog(callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,):
    await dialog_manager.done()
    await callback_query.answer('Каталог')
    await dialog_manager.start(Catalog_levels.level_3, mode=StartMode.RESET_STACK)

async def to_order(callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager):
    await dialog_manager.done()
    await callback.answer('Оформление заказа')
    await callback.message.delete()
    await callback.message.answer('Вы уверены?', reply_markup=yes_no_kb)

