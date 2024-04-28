from aiogram_dialog import DialogManager

from sqlalchemy import select

from src.database.models import async_session, Catalog


async def get_current_products(dialog_manager: DialogManager, **middleware_data):
    dialog_manager.dialog_data['user_id'] = dialog_manager.current_context().start_data.get('user_id')
    price = dialog_manager.current_context().start_data.get('user_price')
    async with async_session() as session:
        db_main_items = await session.scalars(select(Catalog).where(Catalog.price <= price))
        data = {'item': [(f'{item.name} ({item.price} Руб.)', item.id) for item in db_main_items]}
        return data

