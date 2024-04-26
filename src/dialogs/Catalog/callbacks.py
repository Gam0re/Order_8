from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from .states import Catalog_levels
from ...database.requests import orm_add_to_cart
import src.keyboards.default.reply as kb
from src.database.models import async_session, Catalog, lvl2_base, lvl3_base, lvl4_base, lvl5_base
from sqlalchemy import select
import src.database.requests as rq
from ...keyboards.inline.cart import cart_kb


#запись id для уровня 1
async def selected_level1(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["level_1"] = item_id
    await dialog_manager.switch_to(Catalog_levels.level_2)

#запись id для уровня 2
async def selected_level2(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["level_2"] = item_id
    dialog_manager.dialog_data["user_id"] = callback_query.from_user.id
    await dialog_manager.switch_to(Catalog_levels.level_3)

#запись id для уровня 3
async def selected_level3(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["level_3"] = item_id
    await dialog_manager.switch_to(Catalog_levels.level_4)

#запись id для уровня 4
async def selected_level4(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["level_4"] = item_id
    async with async_session() as session:
        lvl2_name = await session.scalar(select(lvl2_base.level_2).where(lvl2_base.id == int(dialog_manager.current_context().dialog_data.get('level_2'))))
        lvl3_name = await session.scalar(select(lvl3_base.level_3).where(lvl3_base.id == int(dialog_manager.current_context().dialog_data.get('level_3'))))
        lvl4_name = await session.scalar(select(lvl4_base.level_4).where(lvl4_base.id == int(dialog_manager.current_context().dialog_data.get('level_4'))))
        db_main = set(await session.scalars(select(Catalog.level_5).where(Catalog.level_2 == lvl2_name, Catalog.level_3 == lvl3_name, Catalog.level_4 == lvl4_name)))
        data = {'lvl5': [(level, await session.scalar(select(lvl5_base.id).where(lvl5_base.level_5 == level))) for level in db_main]}
        if data['lvl5'][0][0] == '':
            dialog_manager.dialog_data["select_items"] = 'level_5'
            await dialog_manager.switch_to(Catalog_levels.select_item)
        else:
            await dialog_manager.switch_to(Catalog_levels.level_5)

#запись id для уровня 5
async def selected_level5(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["level_5"] = item_id
    dialog_manager.dialog_data["select_items"] = 'level_6'
    await dialog_manager.switch_to(Catalog_levels.select_item)
#callback data для 3 уровня для просмотра товаров
async def selected_item3(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["select_items"] = 'level_3'
    await dialog_manager.switch_to(Catalog_levels.select_item)

#callback data для 4 уровня для просмотра товаров
async def selected_item4(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["select_items"] = 'level_4'
    await dialog_manager.switch_to(Catalog_levels.select_item)

#callback data для 5 уровня для просмотра товаров
async def selected_item5(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["select_items"] = 'level_5'
    await dialog_manager.switch_to(Catalog_levels.select_item)

#запись id товара и переход к карточке
async def to_item(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["item_id"] = item_id
    await dialog_manager.switch_to(Catalog_levels.item)

#кнопка для выхода из просмотра товаров
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


#добавление в корзину
async def to_cart(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await orm_add_to_cart(tg_id=callback_query.from_user.id, product_id=int(dialog_manager.current_context().dialog_data.get('item_id')))
    await callback_query.answer("Товар добавлен в корзину")
    await dialog_manager.switch_to(Catalog_levels.select_item)

async def to_main(callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,):
    await dialog_manager.done()
    await callback_query.message.answer("Вас приветствует интернет магазин кондиционеров", reply_markup=kb.start)

async def go_to_cart(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await callback_query.answer('Корзина')
    await dialog_manager.done()
    data = await rq.orm_get_user_carts(callback_query.from_user.id)
    order_price = await rq.get_order_price(callback_query.from_user.id)
    if len(data) > 0:
        page = 0
        media = await rq.orm_get_user_media(callback_query.from_user.id, data[page].product_id, page+1, len(data))
        await callback_query.message.delete()
        await callback_query.message.answer_photo(photo=media['photo'], caption=media['name'], reply_markup=cart_kb(page, order_price))
    else:
        await callback_query.message.delete()
        await callback_query.message.answer(text='Корзина пуста')
