from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from src.data.config import database_url
import pandas as pd
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

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        session = sessionmaker()
        session.configure(bind=engine)
        s = session()
        try:
            with open('severcon_export.csv', 'r') as file:
                data = pd.read_csv(file)

                for i in data:
                    record = Catalog(**{
                        'cond_id' : i[0],
                        'name' : i[1],
                        'image' : i[3],
                        'level_1' : i[4],
                        'level_2' : i[5],
                        'level_3' : i[6],
                        'level_4' : i[7],
                        'level_5' : i[8]
                    })
                    s.add(record) #Add all the records

            s.commit() #Attempt to commit all the records
        except:
            s.rollback() #Rollback the changes on error
        finally:
            s.close() #Close the connection
