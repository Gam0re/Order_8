
from src.database.models import async_session, User, Catalog, Cart
from sqlalchemy import select, or_, delete



async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def orm_add_to_cart(tg_id: int, product_id: int):
    async with async_session() as session:
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

async def orm_get_user_carts(tg_id):
    async with async_session() as session:
        query = select(Cart).filter(Cart.tg_id == tg_id and Cart.status == 'shop')
        result = await session.execute(query)
        return result.scalars().all()


async def orm_delete_from_cart(tg_id: int, product_id: int):
    async with async_session() as session:
        query = delete(Cart).where(Cart.tg_id == tg_id, Cart.product_id == product_id)
        await session.execute(query)
        await session.commit()


async def orm_reduce_product_in_cart(tg_id: int, product_id: int):
    async with async_session() as session:
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
            await orm_delete_from_cart(tg_id, product_id)
            await session.commit()
            return False

async def orm_get_user_media(tg_id, product_id, page, pages):
    async with async_session() as session:
        result = await session.scalar(select(Catalog).where(Catalog.id == product_id))
        quantity = await session.scalar(select(Cart.quantity).where(Cart.product_id == product_id and Cart.tg_id == tg_id))
        return {'photo': result.image,
                'name': f'{result.name}\nКоличество: {quantity}\nСтраница {page} из {pages}'}


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

