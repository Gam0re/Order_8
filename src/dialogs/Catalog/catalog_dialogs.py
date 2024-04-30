from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Row,
    ScrollingGroup,
    Select
)
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import DynamicMedia, StaticMedia
from aiogram.types import ContentType
import operator

from .states import Catalog_levels
from .getters import get_level_4, get_level_5, get_level_3, get_item, get_selected_items
from .callbacks import selected_level3, selected_level4, selected_level5, \
    selected_item3, to_item, back, selected_item4,selected_item5, to_cart, to_main, go_to_cart



Catalog_lvl1 = Dialog(
    Window(
        Const("Пожалуйста, выберите категорию"),
        ScrollingGroup(
            Select(
                id="Level_3",
                items="lvl3",
                item_id_getter=operator.itemgetter(1),
                text=Format("{item[0]}"),
                on_click=selected_level3,
            ),
            id="lvl3_group",
            height=5,
            width=1,
            hide_on_single_page=True
        ),
        Row(Button(Const("На главную"), id="to_main", on_click=to_main), Button(Const("Корзина"), id="go_to_cart", on_click=go_to_cart)),
        state=Catalog_levels.level_3,
        getter=get_level_3,
    ),
    Window(
        Const("Пожалуйста, выберите серию"),
        ScrollingGroup(
            Select(
                id="Level_4",
                items="lvl4",
                item_id_getter=operator.itemgetter(1),
                text=Format("{item[0]}"),
                on_click=selected_level4,
            ),
            id="lvl4_group",
            height=6,
            width=1,
            hide_on_single_page=True
        ),
        Row(Button(Const("На главную"), id="to_main", on_click=to_main), Button(Const("Корзина"), id="go_to_cart", on_click=go_to_cart),
            Back(Const("⬅ Назад"))),
        state=Catalog_levels.level_4,
        getter=get_level_4,
    ),
    Window(
        Const("Пожалуйста, выберите серию"),
        ScrollingGroup(
            Select(
                id="Level_5",
                items="lvl5",
                item_id_getter=operator.itemgetter(1),
                text=Format("{item[0]}"),
                on_click=selected_level5,
            ),
            id="lvl5_group",
            height=6,
            width=1,
            hide_on_single_page=True
        ),
        Row(Button(Const("На главную"), id="to_main", on_click=to_main), Button(Const("Корзина"), id="go_to_cart", on_click=go_to_cart),
            Back(Const("⬅ Назад"))),
        state=Catalog_levels.level_5,
        getter=get_level_5,
    ),
    Window(
        Const("Выберите товар"),
        ScrollingGroup(
            Select(
                id="selected_items",
                items="item",
                item_id_getter=operator.itemgetter(1),
                text=Format("{item[0]}"),
                on_click=to_item,
            ),
            id="selected_items_group",
            height=6,
            width=1,
            hide_on_single_page=True
        ),
        Row(Button(Const("На главную"), id="to_main", on_click=to_main), Button(Const("Корзина"), id="go_to_cart", on_click=go_to_cart),
            Button(Const("⬅ Назад"), id="back", on_click=back)),
        state=Catalog_levels.select_item,
        getter=get_selected_items,
    ),
    Window(
        StaticMedia(
        url=Format('{image}'),
        type=ContentType.PHOTO,
    ),
        Format("Вы выбрали: {name}\n"
               "Цена: {price}\n"
               "Характеристика:\n"
               "{type_comp}\n"
               "{brend}\n"
               "{garant}\n"
               "{cold_pr}\n"
               "{warm_pr}\n"
               "{power_cons_cold}\n"
               "{power_cons_warm}\n"
               "{wifi}\n"),
        Row(Button(Const("В корзину"), id="to_cart", on_click=to_cart), Button(Const("На главную"), id="to_main", on_click=to_main),
            Back(Const("⬅ Назад"))),
        state=Catalog_levels.item,
        getter=get_item,
    ),
)


