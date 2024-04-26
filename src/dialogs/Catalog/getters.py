from src.database.models import async_session, Catalog, lvl1_base, lvl2_base, lvl3_base, lvl4_base, lvl5_base, User
from sqlalchemy import select
from src.utils.funcs import get_image_size, get_image_ratio
from .states import Catalog_levels
from aiogram_dialog import DialogManager


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
        if data['lvl5'][0][0] == '':
            dialog_manager.dialog_data["select_items"] = 'select_items'
            await dialog_manager.switch_to(Catalog_levels.select_item)
            lvl2_name = await session.scalar(select(lvl2_base.level_2).where(lvl2_base.id == int(dialog_manager.current_context().dialog_data.get('level_2'))))
            lvl3_name = await session.scalar(select(lvl3_base.level_3).where(lvl3_base.id == int(dialog_manager.current_context().dialog_data.get('level_3'))))
            lvl4_name = await session.scalar(select(lvl4_base.level_4).where(lvl4_base.id == int(dialog_manager.current_context().dialog_data.get('level_4'))))
            db_main_items = set(await session.scalars(select(Catalog).where(Catalog.level_4 == lvl4_name, Catalog.level_3 == lvl3_name, Catalog.level_2 == lvl2_name, Catalog.level_5 == '')))
            data = {'item': [(item.name, item.id) for item in db_main_items]}
            return data
        else:
            print(data)
            print(data['lvl5'][0][0])
            return data

#получение значений товаров
async def get_selected_items(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        level = dialog_manager.current_context().dialog_data.get('select_items')
        if level == 'level_5':
            lvl2_name = await session.scalar(select(lvl2_base.level_2).where(lvl2_base.id == int(dialog_manager.current_context().dialog_data.get('level_2'))))
            lvl3_name = await session.scalar(select(lvl3_base.level_3).where(lvl3_base.id == int(dialog_manager.current_context().dialog_data.get('level_3'))))
            lvl4_name = await session.scalar(select(lvl4_base.level_4).where(lvl4_base.id == int(dialog_manager.current_context().dialog_data.get('level_4'))))
            db_main_items = set(await session.scalars(select(Catalog).where(Catalog.level_5 == '', Catalog.level_4 == lvl4_name, Catalog.level_3 == lvl3_name, Catalog.level_2 == lvl2_name)))
            data = {'item': [(f'{item.name} ({item.price} Руб.)', item.id) for item in db_main_items]}
            return data
        else:
            lvl2_name = await session.scalar(select(lvl2_base.level_2).where(lvl2_base.id == int(dialog_manager.current_context().dialog_data.get('level_2'))))
            lvl3_name = await session.scalar(select(lvl3_base.level_3).where(lvl3_base.id == int(dialog_manager.current_context().dialog_data.get('level_3'))))
            lvl4_name = await session.scalar(select(lvl4_base.level_4).where(lvl4_base.id == int(dialog_manager.current_context().dialog_data.get('level_4'))))
            lvl5_name = await session.scalar(select(lvl5_base.level_5).where(lvl5_base.id == int(dialog_manager.current_context().dialog_data.get('level_5'))))
            db_main_items = set(await session.scalars(select(Catalog).where(Catalog.level_5 == lvl5_name, Catalog.level_4 == lvl4_name, Catalog.level_3 == lvl3_name, Catalog.level_2 == lvl2_name)))
            data = {'item': [(f'{item.name} ({item.price} Руб.)', item.id) for item in db_main_items]}
            return data


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

        opt = await session.scalar(select(User.opt).where(User.tg_id == int(dialog_manager.current_context().dialog_data.get('user_id'))))
        if opt:
            price = float(db_main.price) * 0.8
        else:
            price = float(db_main.price)

        data = {'name': db_main.name,
                'image': image,
                'price': price,
                'type_comp': f'Тип управления компрессором: {db_main.type_comp}',
                'brend': f'Бренд: {db_main.brend}',
                'garant': f'Гарантия: {db_main.garant} мес.',
                'cold_pr': f'Холодопроизводительность: {db_main.cold_pr} кВт',
                'warm_pr': f'Теплопроизводительность: {db_main.warm_pr} кВт',
                'power_cons_cold': f'Потребляемая мощность (охлаждение): {db_main.power_cons_cold} кВт',
                'power_cons_warm': f'Потребляемая мощность (обогрев): {db_main.power_cons_warm} кВт',
                'wifi': f'Wi-fi: {db_main.wifi}'
                }

        return data
