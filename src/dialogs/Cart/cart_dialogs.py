from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Row,
    ScrollingGroup,
    Select
)
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import StaticMedia
from aiogram.types import ContentType
import operator

from .states import Cart_levels
from .getters import get_products, get_item
from .callbacks import to_main, selected_product, delete, increase, reduce, to_order, to_catalog
from src.handlers.order_registration import checking_phone_number


Cart = Dialog(
    Window(
        Format("Ваша корзина на сумму: {total_price}"),
        ScrollingGroup(
            Select(
                id="select",
                items="products",
                item_id_getter=operator.itemgetter(0),
                text=Format("{item[1]}"),
                on_click=selected_product,
            ),
            id="products_group",
            height=10,
            width=1,
            hide_on_single_page=True
        ),
        Row(Button(Const("На главную"), id="to_main", on_click=to_main), Button(Const("Каталог"), id="to_catalog", on_click=to_catalog)),
        Button(Const("Оформить заказ"), id="to_payment", on_click=checking_phone_number),
        state=Cart_levels.select_products,
        getter=get_products,
    ),
    Window(
        StaticMedia(
        url=Format('{image}'),
        type=ContentType.PHOTO,
    ),
        Format("Вы выбрали: {name}\n"
               "Цена: {price}\n"
               "Количество: {quantity}\n"
               "Итоговая цена: {total_price_card}"),
        Row(Button(Const("Удалить"), id="delete", on_click=delete), Button(Const("+"), id="increase", on_click=increase),
            Button(Const("-"), id="reduce", on_click=reduce)),
        Row(Button(Const("На главную"), id="to_main", on_click=to_main), Button(Const("Каталог"), id="to_catalog", on_click=to_catalog), Back(Const("⬅ Назад"))),
        Button(Const("Оформить заказ"), id="to_payment", on_click=checking_phone_number),
        state=Cart_levels.product_card,
        getter=get_item,
    ),
)

