import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Group
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.media import DynamicMedia

async def categories(on_click, lvl):
    return Group(
        Select(
            Format('{item[0]}'),
            id=f'scroll_group_{lvl}',
            item_id_getter=operator.itemgetter(1),
            items='categories',
            on_click=on_click
        ),
        id=f'categories_ids{lvl}',
        width=2
    )


async def first_category(on_click):
    return Group(
        Select(
            Format('{item[0]}'),
            id='first_lvl_catalog_group',
            item_id_getter=operator.itemgetter(1),
            items='categories',
            on_click=on_click
        ),
        id='first_category_id',
        width=2
    )

async def paginated_products(on_click):
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id = f'products_of',
            item_id_getter=operator.itemgetter(2),
            items='products',
            on_click=on_click
        ),
        id=f'products_of__id',
        width=1, height=4
    )