from aiogram_dialog import DialogManager

from sqlalchemy import select, and_

from src.database.models import async_session, Catalog


async def get_current_products(dialog_manager: DialogManager, **middleware_data):
    price = float(dialog_manager.current_context().start_data.get('user_price'))
    control_type = dialog_manager.current_context().start_data.get('user_control_type')
    appointment_type = dialog_manager.current_context().start_data.get('user_appointment_type')
    async with async_session() as session:
        db_main_items = await session.scalars(select(Catalog).filter(and_(Catalog.price <= price,
                                                                          Catalog.control_type.contains(
                                                                              control_type),
                                                                          Catalog.appointment.contains(
                                                                              appointment_type))))
        data = {'item': [(item.name, item.id) for item in db_main_items]}
        if len(data['item']) ==0:
            db_main_items = await session.scalars(select(Catalog).filter(and_(Catalog.control_type.contains(
                                                                              control_type),
                                                                              Catalog.appointment.contains(
                                                                              appointment_type))))
            data = {'item': [(item.name, item.id) for item in db_main_items]}
        if len(data['item']) ==0:
            db_main_items = await session.scalars(select(Catalog).filter(Catalog.appointment.contains(appointment_type)))
            data = {'item': [(item.name, item.id) for item in db_main_items]}
        return data

