from sqlalchemy import BigInteger, String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from src.data.config import database_url
import pandas as pd
import csv

engine = create_async_engine(url=database_url, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    __allow_unmapped__ = True


class User(Base):
    __tablename__ = 'users'

    __allow_unmapped__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)


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
    group_id: Mapped[int] = mapped_column(BigInteger, nullable=True)

class Groups(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(200), nullable=True)
    super_group_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=True)


"""async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    with open(r'database\severcon_export.csv') as file:
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
"""





