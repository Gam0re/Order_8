from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import BigInteger
from sqlalchemy.orm import joinedload
from src.database.models import async_session, User, Catalog, Cart
from sqlalchemy import select, func, cast, or_, delete



async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def orm_add_to_cart(session: AsyncSession, tg_id: BigInteger, product_id: int):
    query = select(Cart).where(Cart.tg_id == tg_id, Cart.product_id == product_id)
    cart = await session.execute(query)
    cart = cart.scalar()
    if cart:
        cart.quantity += 1
        await session.commit()
        return cart
    else:
        session.add(Cart(tg_id=tg_id, product_id=product_id, quantity=1, status='shop'))
        await session.commit()

async def orm_get_user_carts(session: AsyncSession, tg_id):
    query = select(Cart).filter(Cart.tg_id == tg_id).options(joinedload(Cart.product))
    result = await session.execute(query)
    return result.scalars().all()


async def orm_delete_from_cart(session: AsyncSession, tg_id: int, product_id: int):
    query = delete(Cart).where(Cart.tg_id == tg_id, Cart.product_id == product_id)
    await session.execute(query)
    await session.commit()


async def orm_reduce_product_in_cart(session: AsyncSession, tg_id: int, product_id: int):
    query = select(Cart).where(Cart.tg_id == tg_id, Cart.product_id == product_id)
    cart = await session.execute(query)
    cart = cart.scalar()

    if not cart:
        return
    if cart.quantity > 1:
        cart.quantity -= 1
        await session.commit()
        return True
    else:
        await orm_delete_from_cart(session, user_id, product_id)
        await session.commit()
        return False


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
