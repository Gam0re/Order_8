from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Row,
    ScrollingGroup,
    Select,
)
from aiogram_dialog.widgets.text import Const, Format
import operator

from .states import Catalog_levels
from .getters import get_level_1, get_level_2, get_level_4, get_level_5, get_level_3, get_item, get_selected_items
from .callbacks import selected_level1, selected_level2, selected_level3, selected_level4, selected_level5, \
    selected_item3, to_item, back, selected_item4,selected_item5, to_cart



Catalog_lvl1 = Dialog(
    Window(
        Const("Пожалуйста выбирите категорию"),
        ScrollingGroup(
            Select(
                id="level_1",
                items="lvl1",
                item_id_getter=operator.itemgetter(1),
                on_click=selected_level1,
                text=Format("{item[0]}"),
            ),
            id="lvl1_group",
            height=6,
            width=1
        ),

        getter=get_level_1,
        state=Catalog_levels.level_1,
    ),
    Window(
        Const("Пожалуйста выбирите категорию"),
        ScrollingGroup(
            Select(
                id="Level_2",
                items="lvl2",
                item_id_getter=operator.itemgetter(1),
                text=Format("{item[0]}"),
                on_click=selected_level2,
            ),
            id="lvl2_group",
            height=6,
            width=1,
        ),
        Back(Const("⬅ Назад")),
        state=Catalog_levels.level_2,
        getter=get_level_2,
    ),
    Window(
        Const("Пожалуйста выбирите категорию"),
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
        ),
        Row(Button(Const("Посмотреть товары"), id="confirm", on_click=selected_item3),
            Back(Const("⬅ Назад"))),
        state=Catalog_levels.level_3,
        getter=get_level_3,
    ),
    Window(
        Const("Пожалуйста выбирите категорию"),
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
        ),
        Row(Button(Const("Посмотреть товары"), id="confirm", on_click=selected_item4),
            Back(Const("⬅ Назад"))),
        state=Catalog_levels.level_4,
        getter=get_level_4,
    ),
    Window(
        Const("Пожалуйста выбирите категорию"),
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
        ),
        Row(Button(Const("Посмотреть товары"), id="confirm", on_click=selected_item5),
            Back(Const("⬅ Назад"))),
        state=Catalog_levels.level_5,
        getter=get_level_5,
    ),
    Window(
        Const("Выбирите товар"),
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
        ),
        Button(Const("⬅ Назад"), id="back", on_click=back),
        state=Catalog_levels.select_item,
        getter=get_selected_items,
    ),
    Window(
        Format("Вы выбрали: {name}"),
        Row(Button(Const("В корзину"), id="to_cart", on_click=to_cart),
            Back(Const("⬅ Назад"))),
        state=Catalog_levels.item,
        getter=get_item,
    ),
)


