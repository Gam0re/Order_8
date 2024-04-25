from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Row,
    ScrollingGroup,
    Select,
)
from aiogram_dialog.widgets.text import Const, Format
from aiogram.types import ContentType
import operator
from src.dialogs.Selection.callbacks import to_main, to_item, to_cart
from src.dialogs.Selection.getters import get_current_products
from src.dialogs.Selection.selection_states import SelectionStates
from src.dialogs.Catalog.getters import get_item

selection = Dialog(
    Window(
        Const('Выберете товары'),
        ScrollingGroup(Select(
                id="selected_items",
                items="item",
                item_id_getter=operator.itemgetter(1),
                on_click=to_item,
                text=Format("{item[0]}"),
            ),
            id="selected_items_group",
            height=6,
            width=1
        ),
        Button(Const("На главную"), id="to_main", on_click=to_main),
        getter=get_current_products,
        state=SelectionStates.searching_products,),
    Window(
        StaticMedia(
            url=Format('{image}'),
            type=ContentType.PHOTO,
        ),
    Format("Вы выбрали: {name}\n"
           "Описание:\n"
           "{description}\n"
           "Цена: {price} Руб."),
        Row(Button(Const("В корзину"), id="to_cart", on_click=to_cart), Button(Const("На главную"), id="to_main", on_click=to_main),
            Back(Const("⬅ Назад"))),
        state=SelectionStates.view_product,
        getter=get_item,
        )
    )