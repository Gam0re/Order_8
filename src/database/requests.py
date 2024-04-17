from src.database.models import async_session, User, Catalog
from sqlalchemy import select


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def get_level_1():
    async with async_session() as session:
        return await session.scalars(select(Catalog.level_1))

async def get_level_2():
    async with async_session() as session:
        return await session.scalars(select(Catalog.level_2))

async def get_level_3(level_2):
    async with async_session() as session:
        return await session.scalars(select(Catalog.level_3).where(Catalog.level_2 == level_2))

async def get_level_4(level_2, level_3):
    async with async_session() as session:
        return await session.scalars(select(Catalog.level_4).where(Catalog.level_2 == level_2 and Catalog.level_3 == level_3))

async def get_level_5(level_2, level_3, level_4):
    async with async_session() as session:
        return await session.scalars(select(Catalog.level_5).where(Catalog.level_2 == level_2 and Catalog.level_3 == level_3 and Catalog.level_4 == level_4))

async def get_names(level_2, level_3, level_4, level_5):
    async with async_session() as session:
        return await session.scalars(select(Catalog.name).where(Catalog.level_5 == level_5 and Catalog.level_4 == level_4))

async def get_item(name):
    async with async_session() as session:
        return await session.scalar(select(Catalog.image).where(Catalog.name == name))
