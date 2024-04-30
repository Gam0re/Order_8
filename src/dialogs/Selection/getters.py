from aiogram_dialog import DialogManager

from sqlalchemy import select

from src.database.models import async_session, Catalog


async def get_current_products(dialog_manager: DialogManager, **middleware_data):
    dialog_manager.dialog_data['user_id'] = dialog_manager.current_context().start_data.get('user_id')
    price = dialog_manager.current_context().start_data.get('user_price')
    type_comp = dialog_manager.current_context().start_data.get('user_type_comp')
    async with async_session() as session:
        if type_comp == 'Инверторный':
            db_main_items = await session.scalars(select(Catalog).where(Catalog.price <= price, Catalog.type_comp == 'Инверторный'))
        else:
            db_main_items = await session.scalars(
                select(Catalog).where(Catalog.price <= price, Catalog.type_comp != 'Инверторный'))
        data = {'item': [(f'{item.name.split()[-1]} ({item.price} Руб.)', item.id) for item in db_main_items]}
        return data

