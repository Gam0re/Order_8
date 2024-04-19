from aiogram_dialog.widgets.kbd import Button

from aiogram_dialog.widgets.text import Const

from typing import Any

from aiogram_dialog import ChatEvent, DialogManager
import src.database.requests as rq
level_1_dict = {}
level_2_dict = {}
level_3_dict = {}
level_4_dict = {}
level_5_dict = {}
name_dict = {}

async def level1_changed(
    callback: ChatEvent,
    select: Any,
    manager: DialogManager,
    item_id: str,
):
    manager.dialog_data["level_1"] = item_id
    await manager.next()

async def lvl1_buttons_creator():
    btn_quantity = set(await rq.get_level_1())
    buttons = []
    count = 0
    for i in btn_quantity:
        level_1_dict[count] = i
        buttons.append(Button(Const(i), id=str(count), on_click=level1_changed))
        count += 1
    return buttons


async def level2_changed(
    callback: ChatEvent,
    select: Any,
    manager: DialogManager,
    item_id: str,
):
    manager.dialog_data["level_2"] = item_id
    await manager.next()

def lvl2_buttons_creator():
    btn_quantity = set(await rq.get_level_2())
    buttons = []
    count = 0
    for i in btn_quantity:
        level_2_dict[count] = i
        buttons.append(Button(Const(i), id=str(count), on_click=level2_changed))
        count += 1
    return buttons
