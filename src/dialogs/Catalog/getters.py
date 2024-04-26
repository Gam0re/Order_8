from src.database.models import async_session, Catalog, lvl1_base, lvl2_base, lvl3_base, lvl4_base, lvl5_base
from sqlalchemy import select
import requests
from PIL import Image
from io import BytesIO

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

async def get_image_size(url):
    try:
        response = requests.head(url)
        headers = response.headers
        content_length = headers.get('Content-Length')
        if content_length:
            size_in_bytes = int(content_length)
            size_in_mb = size_in_bytes / 1048576
            return size_in_mb
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None

async def get_image_ratio(url):
    try:
        response = requests.get(url)
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        width, height = image.size
        aspect_ratio = width / height
        return width, height, aspect_ratio
    except Exception as e:
        print("Error:", e)
        return None, None, None


#получение карточки товара
async def get_item(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        db_main = await session.scalar(select(Catalog).where(Catalog.id == int(dialog_manager.current_context().dialog_data.get('item_id'))))
        if db_main.image == '':
            image = 'https://cdn-icons-png.flaticon.com/512/4054/4054617.png'
        else:
            size = await get_image_size(db_main.image)
            ratio = await get_image_ratio(db_main.image)
            if (size and size > 10) or (ratio[0] and ratio[0] + ratio[1] > 10000 or ratio[2] > 20):
                image = 'https://cdn-icons-png.flaticon.com/512/4054/4054617.png'
            else:
                image = db_main.image

        if len(db_main.description) > 300:
            description = db_main.description[0:300]
        elif len(db_main.description) < 300 and db_main.description != '':
            description = db_main.description
        else:
            description = 'Описание товара отсутствует'
        data = {'name': db_main.name,
                'image': image,
                'price': db_main.price,
                'description': description}
        return data
