from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select

from .states import Catalog_levels

async def selected_level1(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["level_1"] = item_id
    await dialog_manager.switch_to(Catalog_levels.level_2)

async def selected_level2(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["level_2"] = item_id
    await dialog_manager.switch_to(Catalog_levels.level_3)

async def selected_level3(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["level_3"] = item_id
    await dialog_manager.switch_to(Catalog_levels.level_4)

async def selected_level4(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["level_4"] = item_id
    await dialog_manager.switch_to(Catalog_levels.level_5)

async def selected_level5(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["level_5"] = item_id
    dialog_manager.dialog_data["select_items"] = 'level_6'
    await dialog_manager.switch_to(Catalog_levels.select_item)

async def selected_item3(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["select_items"] = 'level_3'
    await dialog_manager.switch_to(Catalog_levels.select_item)

async def selected_item4(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["select_items"] = 'level_4'
    await dialog_manager.switch_to(Catalog_levels.select_item)

async def selected_item5(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["select_items"] = 'level_5'
    await dialog_manager.switch_to(Catalog_levels.select_item)

async def to_item(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["item_id"] = item_id
    await dialog_manager.switch_to(Catalog_levels.item)

async def back(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    if dialog_manager.current_context().dialog_data.get('select_items') == 'level_3':
        await dialog_manager.switch_to(Catalog_levels.level_3)
    elif dialog_manager.current_context().dialog_data.get('select_items') == 'level_4':
        await dialog_manager.switch_to(Catalog_levels.level_4)
    elif dialog_manager.current_context().dialog_data.get('select_items') == 'level_5':
        await dialog_manager.switch_to(Catalog_levels.level_5)
    else:
        await dialog_manager.switch_to(Catalog_levels.level_5)

async def to_cart(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await callback_query.message.answer("Товар добавлен в корзину")
    await dialog_manager.done()
