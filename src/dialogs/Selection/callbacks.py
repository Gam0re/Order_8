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
    await orm_add_to_cart(tg_id=callback_query.from_user.id, product_id=int(dialog_manager.current_context().dialog_data.get('item_id')))
    await callback_query.answer("Товар добавлен в корзину")
    await dialog_manager.switch_to(SelectionStates.searching_products)

async def to_main(callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,):
    await dialog_manager.done()
    await callback_query.message.answer("Вас приветствует интернет магазин кондиционеров", reply_markup=kb.start)

async def to_item(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["item_id"] = item_id
    await dialog_manager.switch_to(SelectionStates.view_product)