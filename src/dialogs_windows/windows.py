from aiogram_dialog import Window, Data, DialogManager, ShowMode

from typing import Any

from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Cancel, Back
from aiogram_dialog.widgets.media import DynamicMedia

from src.states.dialog import dialogFSM, buyFSM, choosingFSM
from src.database import requests as rq

from src.dialogs_windows import keyboards, selected


async def categories_window(lvl):
    if lvl == 1:
        state = dialogFSM.level1
    elif lvl == 2:
        state = dialogFSM.level2
    elif lvl == 3:
        state = dialogFSM.level3
    elif lvl == 4:
        state = dialogFSM.level4
    elif lvl == 5:
        state = dialogFSM.level5
    return Window(
        Const(f'Выберете раздел'),
        await keyboards.categories(selected.on_chosen_category, lvl),
        Back(Const('Назад'), on_click=selected.go_back),
        state=state,
        getter=rq.get_categories,
    )

async def tovari_window():
    return Window(
        Const('товары'),
        await keyboards.paginated_products(selected.on_chosen_product),
        Cancel(Const('<<Венуться к категориям'),
            id='cancel_s_t_select_ct',
            result={'switch_to': 1}
               ),
        state=choosingFSM.choose,
        getter=rq.get_products
    )
async def first_category_window():
    return Window(
        Const('Выберете раздел'),
        await keyboards.first_category(selected.on_chosen_category),
        Cancel(Const('назад')),
        state=dialogFSM.first_level_state,
        getter=rq.get_categories_first
    )

async def on_process_result(data: Data, result: Any, manager: DialogManager):
    id = int(data.get('item_id'))
    lvl = await rq.get_lvl(id)
    manager.dialog_data['categories'] = await rq.get_previous_category(dialog_manager=manager)
    manager.dialog_data['is_from_product'] = True
    if result:
        switch_to_window = result.get('switch_to')
        if lvl == 1:
            manager.show_mode = ShowMode.SEND
            await manager.switch_to(dialogFSM.first_level_state)
        elif lvl == 2:
            manager.show_mode = ShowMode.SEND
            await manager.switch_to(dialogFSM.level2)
        elif lvl == 3:
            manager.show_mode = ShowMode.SEND
            await manager.switch_to(dialogFSM.level3)
        elif lvl == 4:
            manager.show_mode = ShowMode.SEND
            await manager.switch_to(dialogFSM.level4)
        elif lvl == 5:
            manager.show_mode = ShowMode.SEND
            await manager.switch_to(dialogFSM.level5)