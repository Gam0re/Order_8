from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy import insert, update
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from src.data.config import database_url

engine = create_async_engine(url=database_url, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    __allow_unmapped__ = True


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)


async def async_main():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def insert_name_and_phone(tg_id, name, phone):
    async with engine.connect() as conn:
        stmt = (
            update(User).
            where(User.tg_id==tg_id).
            values(name=name, phone=phone)
        )
        await conn.execute(stmt)
        await conn.commit()
async def update_name(tg_id, name):
    async with engine.connect() as conn:
        stmt = (
            update(User).
            where(User.tg_id==tg_id).
            values(name=name)
        )
        await conn.execute(stmt)
        await conn.commit()
async def update_phone(tg_id, phone):
    async with engine.connect() as conn:
        stmt = (
            update(User).
            where(User.tg_id==tg_id).
            values(phone=phone)
        )
        await conn.execute(stmt)
        await conn.commit()
