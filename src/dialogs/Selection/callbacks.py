from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select

from src.database.requests import orm_add_to_cart
from src.dialogs.Selection.selection_states import SelectionStates

import src.keyboards.default.reply as kb
from aiogram.fsm.context import FSMContext

async def to_cart(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await orm_add_to_cart(tg_id=callback_query.from_user.id, product_id=int(dialog_manager.current_context().dialog_data.get('item_id')), quant=dialog_manager.dialog_data["quant"])
    await callback_query.answer("Товар добавлен в корзину")
    await dialog_manager.switch_to(SelectionStates.searching_products)

async def to_main(callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,):
    await dialog_manager.done()
    await callback_query.message.answer('Вас приветствует интернет магазин кондиционеров "Центр климата"', reply_markup=kb.start)

async def to_item(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["item_id"] = item_id
    dialog_manager.dialog_data["quant"] = 1
    await dialog_manager.switch_to(SelectionStates.view_product)

async def increment(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["quant"] += 1

async def decrement(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    if dialog_manager.dialog_data["quant"] > 1:
        dialog_manager.dialog_data["quant"] -= 1
    else:
        await callback_query.answer('Нельзя уменьшить количество')
        dialog_manager.dialog_data["quant"] = 1

async def quant(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await callback_query.answer(f'Количество: {dialog_manager.dialog_data["quant"]}')
