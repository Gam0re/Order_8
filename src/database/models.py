from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from src.data.config import database_url
from src.data.config import DB_USER, DB_NAME, DB_HOST, DB_PASS, DB_PORT
import pandas as pd
import csv
from sqlalchemy import select

import psycopg2

conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER, password=DB_PASS,
                        host=DB_HOST, port=DB_PORT
)

conn.autocommit = True
cursor = conn.cursor()

engine = create_async_engine(url=database_url, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)

class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(nullable=True)
    product_id: Mapped[int] = mapped_column(nullable=True)
    quantity: Mapped[int]
    status: Mapped[str] = mapped_column(String(20), nullable=True)

class Catalog(Base):
    __tablename__ = 'catalog'

    id: Mapped[int] = mapped_column(primary_key=True)
    cond_id: Mapped[int] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    image: Mapped[str] = mapped_column(String(200), nullable=True)
    level_1: Mapped[str] = mapped_column(String(100), nullable=True)
    level_2: Mapped[str] = mapped_column(String(100), nullable=True)
    level_3: Mapped[str] = mapped_column(String(100), nullable=True)
    level_4: Mapped[str] = mapped_column(String(100), nullable=True)
    level_5: Mapped[str] = mapped_column(String(100), nullable=True)

class lvl1_base(Base):
    __tablename__ = 'level_1'

    id: Mapped[int] = mapped_column(primary_key=True)
    level_1: Mapped[str] = mapped_column(String(100), nullable=True)

class lvl2_base(Base):
    __tablename__ = 'level_2'

    id: Mapped[int] = mapped_column(primary_key=True)
    level_2: Mapped[str] = mapped_column(String(100), nullable=True)

class lvl3_base(Base):
    __tablename__ = 'level_3'

    id: Mapped[int] = mapped_column(primary_key=True)
    level_3: Mapped[str] = mapped_column(String(100), nullable=True)

class lvl4_base(Base):
    __tablename__ = 'level_4'

    id: Mapped[int] = mapped_column(primary_key=True)
    level_4: Mapped[str] = mapped_column(String(100), nullable=True)

class lvl5_base(Base):
    __tablename__ = 'level_5'

    id: Mapped[int] = mapped_column(primary_key=True)
    level_5: Mapped[str] = mapped_column(String(100), nullable=True)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open(r'src\database\severcon_export.csv') as file:
        reader = csv.reader(file, delimiter='\t')
        header = list(next(reader))
        all_products = []

        for row in reader:
            new_line = {k: v for k, v in zip(header, row)}
            all_products.append(new_line)
        df = pd.DataFrame(all_products)

        async with async_session() as session:
            for index, row in df.iterrows():
                record = Catalog(**{
                    'cond_id': int(row[0]),
                    'name': row[1],
                    'image': row[3],
                    'level_1': row[4],
                    'level_2': row[5],
                    'level_3': row[6],
                    'level_4': row[7],
                    'level_5': row[8]
                })
                session.add(record)

            await session.commit()

            level_1 = set(await session.scalars(select(Catalog.level_1)))
            for level in level_1:
                record_lvl1 = lvl1_base(**{
                    'level_1': level
                })
                session.add(record_lvl1)
            await session.commit()

            level_2 = set(await session.scalars(select(Catalog.level_2)))
            for level in level_2:
                record_lvl2 = lvl2_base(**{
                    'level_2': level
                })
                session.add(record_lvl2)
            await session.commit()

            level_3 = set(await session.scalars(select(Catalog.level_3)))
            for level in level_3:
                record_lvl3 = lvl3_base(**{
                    'level_3': level
                })
                session.add(record_lvl3)
            await session.commit()

            level_4 = set(await session.scalars(select(Catalog.level_4)))
            for level in level_4:
                record_lvl4 = lvl4_base(**{
                    'level_4': level
                })
                session.add(record_lvl4)
            await session.commit()

            level_5 = set(await session.scalars(select(Catalog.level_5)))
            for level in level_5:
                record_lvl5 = lvl5_base(**{
                    'level_5': level
                })
                session.add(record_lvl5)
            await session.commit()
