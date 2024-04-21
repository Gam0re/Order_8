from aiogram import types

from aiogram_dialog import DialogManager

from aiogram_dialog.widgets.kbd import Select, Button

import src.states.dialog as dialog_states
from src.database.requests import get_lvl, is_this_last_lvl, get_categories, get_previous_category


async def go_back(c: types.CallbackQuery, button: Button, manager: DialogManager):

    item_id = manager.dialog_data.get('item_id')
    manager.dialog_data['is_it_back'] = True
    lvl = int(await get_lvl(item_id))
    if lvl == 2:
        state = dialog_states.dialogFSM.first_level_state
    elif lvl == 3:
        state = dialog_states.dialogFSM.level2
    elif lvl == 4:
        state = dialog_states.dialogFSM.level3
    elif lvl == 5:
        state = dialog_states.dialogFSM.level4
    await manager.switch_to(state)


async def on_chosen_category(c: types.CallbackQuery,widget: Select, manager: DialogManager, item_id:str):
    item_id = int(item_id)
    manager.dialog_data['item_id'] = item_id
    lvl = await get_lvl(item_id)
    if lvl == 2:
        state = dialog_states.dialogFSM.level2
    elif lvl == 3:
        state = dialog_states.dialogFSM.level3
    elif lvl == 4:
        state = dialog_states.dialogFSM.level4
    if lvl == 5 or await is_this_last_lvl(item_id):
        await manager.start(dialog_states.choosingFSM.choose, data={
            'item_id':item_id, 'categories': await get_previous_category(dialog_manager=manager)
        })
    else:
        await manager.switch_to(state)


async def on_chosen_product(c: types.CallbackQuery,widget: Select, manager: DialogManager):
    name = manager.dialog_data.get('name')
    await manager.switch_to(dialog_states.buyFSM.enter_amount)