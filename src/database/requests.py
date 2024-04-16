from src.database.models import async_session, User, Catalog
from sqlalchemy import select, func, cast, or_
import re



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


async def get_models(model_name):
    async with async_session() as session:
        query = (
            select(
                Catalog
            )
            .filter(or_(Catalog.name.contains(model_name)))
        )
        print(query.compile(compile_kwargs={'literal_binds': True}))
        res = await session.execute(query)
        result = res.all()
