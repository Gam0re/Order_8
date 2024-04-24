from src.database.models import async_session, Catalog, lvl1_base, lvl2_base, lvl3_base, lvl4_base, lvl5_base
from sqlalchemy import select

from aiogram_dialog import DialogManager

class level_1:
    name: str
    id: int

#получение значений для 1 уровня
async def get_level_1(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        db_lvl1 = await session.scalars(select(lvl1_base))
        data = {'lvl1': [(level.level_1, level.id) for level in db_lvl1]}
        return data

#получение значений для 2 уровня
async def get_level_2(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        db_lvl2 = await session.scalars(select(lvl2_base))
        data = {'lvl2': [(level.level_2, level.id) for level in db_lvl2]}
        return data

#получение значений для 3 уровня
async def get_level_3(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        lvl2_name = await session.scalar(select(lvl2_base.level_2).where(lvl2_base.id == int(dialog_manager.current_context().dialog_data.get('level_2'))))
        db_main = set(await session.scalars(select(Catalog.level_3).where(Catalog.level_2 == lvl2_name)))
        db_main_items = set(await session.scalars(select(Catalog).where(Catalog.level_2 == lvl2_name, Catalog.level_3 == '')))
        data = {'lvl3': [(level, await session.scalar(select(lvl3_base.id).where(lvl3_base.level_3 == level))) for level in db_main],
                'lvl3_item': [(item.name, item.id) for item in db_main_items]}
        return data

#получение значений для 4 уровня
async def get_level_4(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        lvl2_name = await session.scalar(select(lvl2_base.level_2).where(lvl2_base.id == int(dialog_manager.current_context().dialog_data.get('level_2'))))
        lvl3_name = await session.scalar(select(lvl3_base.level_3).where(lvl3_base.id == int(dialog_manager.current_context().dialog_data.get('level_3'))))
        db_main = set(await session.scalars(select(Catalog.level_4).where(Catalog.level_2 == lvl2_name, Catalog.level_3 == lvl3_name)))
        db_main_items = set(await session.scalars(select(Catalog).where(Catalog.level_2 == lvl2_name, Catalog.level_3 == lvl3_name, Catalog.level_4 == '')))
        data = {'lvl4': [(level, await session.scalar(select(lvl4_base.id).where(lvl4_base.level_4 == level))) for level in db_main],
                'lvl4_item': [(item.name, item.id) for item in db_main_items]}
        return data

#получение значений для 5 уровня
async def get_level_5(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        lvl2_name = await session.scalar(select(lvl2_base.level_2).where(lvl2_base.id == int(dialog_manager.current_context().dialog_data.get('level_2'))))
        lvl3_name = await session.scalar(select(lvl3_base.level_3).where(lvl3_base.id == int(dialog_manager.current_context().dialog_data.get('level_3'))))
        lvl4_name = await session.scalar(select(lvl4_base.level_4).where(lvl4_base.id == int(dialog_manager.current_context().dialog_data.get('level_4'))))
        db_main = set(await session.scalars(select(Catalog.level_5).where(Catalog.level_2 == lvl2_name, Catalog.level_3 == lvl3_name, Catalog.level_4 == lvl4_name)))
        data = {'lvl5': [(level, await session.scalar(select(lvl5_base.id).where(lvl5_base.level_5 == level))) for level in db_main]}
        return data

#получение значений товаров
async def get_selected_items(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        level = dialog_manager.current_context().dialog_data.get('select_items')
        if level == 'level_3':
            lvl2_name = await session.scalar(select(lvl2_base.level_2).where(lvl2_base.id == int(dialog_manager.current_context().dialog_data.get('level_2'))))
            db_main_items = await session.scalars(select(Catalog).where(Catalog.level_2 == lvl2_name, Catalog.level_3 == ''))
            data = {'item': [(item.name, item.id) for item in db_main_items]}
        elif level == 'level_4':
            lvl2_name = await session.scalar(select(lvl2_base.level_2).where(lvl2_base.id == int(dialog_manager.current_context().dialog_data.get('level_2'))))
            lvl3_name = await session.scalar(select(lvl3_base.level_3).where(lvl3_base.id == int(dialog_manager.current_context().dialog_data.get('level_3'))))
            db_main_items = set(await session.scalars(select(Catalog).where(Catalog.level_3 == lvl3_name, Catalog.level_2 == lvl2_name, Catalog.level_4 == '')))
            data = {'item': [(item.name, item.id) for item in db_main_items]}
        elif level == 'level_5':
            lvl2_name = await session.scalar(select(lvl2_base.level_2).where(lvl2_base.id == int(dialog_manager.current_context().dialog_data.get('level_2'))))
            lvl3_name = await session.scalar(select(lvl3_base.level_3).where(lvl3_base.id == int(dialog_manager.current_context().dialog_data.get('level_3'))))
            lvl4_name = await session.scalar(select(lvl4_base.level_4).where(lvl4_base.id == int(dialog_manager.current_context().dialog_data.get('level_4'))))
            db_main_items = set(await session.scalars(select(Catalog).where(Catalog.level_4 == lvl4_name, Catalog.level_3 == lvl3_name, Catalog.level_2 == lvl2_name, Catalog.level_5 == '')))
            data = {'item': [(item.name, item.id) for item in db_main_items]}
        else:
            lvl2_name = await session.scalar(select(lvl2_base.level_2).where(lvl2_base.id == int(dialog_manager.current_context().dialog_data.get('level_2'))))
            lvl3_name = await session.scalar(select(lvl3_base.level_3).where(lvl3_base.id == int(dialog_manager.current_context().dialog_data.get('level_3'))))
            lvl4_name = await session.scalar(select(lvl4_base.level_4).where(lvl4_base.id == int(dialog_manager.current_context().dialog_data.get('level_4'))))
            lvl5_name = await session.scalar(select(lvl5_base.level_5).where(lvl5_base.id == int(dialog_manager.current_context().dialog_data.get('level_5'))))
            db_main_items = set(await session.scalars(select(Catalog).where(Catalog.level_5 == lvl5_name, Catalog.level_4 == lvl4_name, Catalog.level_3 == lvl3_name, Catalog.level_2 == lvl2_name)))
            data = {'item': [(item.name, item.id) for item in db_main_items]}
        return data

#получение карточки товара
async def get_item(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        db_main = await session.scalar(select(Catalog).where(Catalog.id == int(dialog_manager.current_context().dialog_data.get('item_id'))))
        data = {'name': db_main.name,
                'image': db_main.image,
                'price': db_main.price,
                'description': db_main.description}
        return data
