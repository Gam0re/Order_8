from src.database.models import async_session, User, Catalog, Groups
from sqlalchemy import select, func, cast, or_
import re

from aiogram_dialog import DialogManager
import src.states.dialog as dialog_states


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def update_name_and_phone(tg_id, **kwargs):
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        user = await session.get(User, user_id)
        for data_type, data in kwargs.items():
            if data_type=='name':
                user.name = data
            if data_type=='phone':
                user.phone = data
            await session.commit()

async def get_name(tg_id):
    async with async_session() as session:
        name = await session.scalar(select(User.name).where(User.tg_id == tg_id))
    return name

async def get_number(tg_id):
    async with async_session() as session:
        phone = await session.scalar(select(User.phone).where(User.tg_id == tg_id))
    return phone

async def get_lvl(id):
    async with async_session() as session:
        lvl = await session.scalar(select(Groups.level).where(Groups.id == id))
    return lvl

async def is_this_last_lvl(id):
    async with async_session() as session:
        result = await session.scalar(select(Groups.id).where(Groups.super_group_id==id))
    return not result

async def get_categories(dialog_manager: DialogManager, **middleware_data):
    async with async_session() as session:
        try:
            categories = dialog_manager.current_context().dialog_data.pop('categories')
            data = categories
        except:
            is_it_back = dialog_manager.current_context().dialog_data.get('is_it_back')
            is_from_product = dialog_manager.current_context().dialog_data.get('is_from_product')
            id = dialog_manager.current_context().dialog_data.get('item_id')
            group_id = await session.scalar(select(Groups.super_group_id).where(Groups.id == id))
            super_group_id = await session.scalar(select(Groups.super_group_id).where(Groups.id == group_id))
            if is_from_product:
                stmt = select(Groups).filter(Groups.super_group_id == super_group_id)
                dialog_manager.dialog_data['item_id'] = group_id
            elif is_it_back:
                stmt = select(Groups).filter(Groups.super_group_id == group_id)
                dialog_manager.dialog_data['item_id'] = group_id
            else:
                stmt = select(Groups).filter(Groups.super_group_id == id)
            result = await session.execute(stmt)
            categories = result.all()
            data = {'categories': [
                (category[0].description, category[0].id)
                for category in categories
                ]
            }
            dialog_manager.dialog_data['is_from_product'] = False
        dialog_manager.dialog_data['is_it_back']=False
        if data:
            return data


async def get_products(dialog_manager: DialogManager, **middleware_data):
    async with async_session() as session:
        id = dialog_manager.current_context().start_data.get('item_id')
        stmt = select(Catalog).filter(Catalog.group_id == id)
        result = await session.execute(stmt)
        products = result.all()
        data = {'products':[
            (product[0].name, product[0].image, product[0].id)
            for product in products
        ]}
        return data

async def get_categories_first(dialog_manager: DialogManager, **middleware_data):
    async with async_session() as session:
        name = 'Системы кондиционирования'
        group_id = await session.scalar(select(Groups.id).where(Groups.description == name))
        stmt = select(Groups).filter(Groups.super_group_id == group_id)
        result = await session.execute(stmt)
        categories = result.all()
        data = {'categories':[
            (category[0].description, category[0].id)
            for category in categories
            ]
        }
        if data:
            return data

async def get_previous_category(dialog_manager: DialogManager, **middleware_data):
    async with async_session() as session:
        id = dialog_manager.current_context().dialog_data.get('item_id')
        group_id = await session.scalar(select(Groups.super_group_id).where(Groups.id == id))
        stmt = select(Groups).filter(Groups.super_group_id == group_id)
        result = await session.execute(stmt)
        categories = result.all()
        data = {'categories': [
            (category[0].description, category[0].id)
            for category in categories
        ]
        }
        if data:
            return data


