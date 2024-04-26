from src.utils.funcs import get_image_ratio, get_image_size
from src.database.models import async_session, User, Catalog, Cart
from sqlalchemy import select, or_, delete, func, and_,update




async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, opt=False))
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
        query = select(Cart).where(Cart.tg_id == tg_id, Cart.status == 'shop')
        result = await session.execute(query)
        return result.scalars().all()


async def orm_delete_from_cart(tg_id: int, product_id: int):
    async with async_session() as session:
        query = delete(Cart).where(Cart.tg_id == tg_id, Cart.product_id == product_id, Cart.status == 'shop')
        await session.execute(query)
        await session.commit()


async def orm_reduce_product_in_cart(tg_id: int, product_id: int):
    async with async_session() as session:
        query = select(Cart).where(Cart.tg_id == tg_id, Cart.product_id == product_id, Cart.status == 'shop')
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
        quantity = await session.scalar(select(Cart.quantity).where(Cart.product_id == product_id, Cart.tg_id == tg_id, Cart.status == 'shop'))
        total_price = float(quantity) * float(result.price)
        if result.image == '':
            image = 'https://cdn-icons-png.flaticon.com/512/4054/4054617.png'
        else:
            size = await get_image_size(result.image)
            ratio = await get_image_ratio(result.image)
            if (size and size > 10) or (ratio[0] and ratio[0] + ratio[1] > 10000 or ratio[2] > 20):
                image = 'https://cdn-icons-png.flaticon.com/512/4054/4054617.png'
            else:
                image = result.image
        return {'photo': image,
                'name': f'{result.name}\nКоличество: {quantity}\nЦена: {total_price} Руб.\nСтраница {page} из {pages}'}

async def orm_update_status(tg_id, from_status, to_status):
    async with async_session() as session:
        query = select(Cart).where(Cart.tg_id == tg_id, Cart.status == from_status)
        carts = await session.execute(query)
        carts = carts.scalars()

        for cart in carts:
            cart.status = to_status
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

async def get_orders(tg_id, status):
    async with async_session() as session:
        ids = await session.scalars(select(Cart.product_id).where(Cart.tg_id == tg_id, Cart.status == status))
        print(f'---------------------{await session.scalar(select(Cart.status).where(Cart.tg_id == tg_id))}-----------------------_')
        text = ''
        for product_id in ids:
            text += await session.scalar(select(Catalog.name).where(Catalog.id == product_id))
            text += '\n'
        return text

async def get_product(prod_id):
    async with async_session() as session:
        query = select(Catalog).where(Catalog.id == prod_id)
        result = await session.execute(query)
        return result.scalar()


async def get_order_price(tg_id):
    data = await orm_get_user_carts(tg_id)
    order_price = 0
    for order in data:
        order_price += float((await get_product(order.product_id)).price) * int(order.quantity)
    return order_price
async def get_max_and_min():
    async with async_session() as session:
        max_price = await session.scalar(func.max(Catalog.price))
        min_price = await session.scalar(func.min(Catalog.price))
        return max_price, min_price

async def get_control_types():
    async with async_session() as session:
        types = set(await session.scalars(select(Catalog.control_type)))
        return types

async def get_appointment_types():
    async with async_session() as session:
        types = set(await session.scalars(select(Catalog.appointment)))
        right_types = []
        for type in types:
            for one_type in type.split('|'):
                right_types.append(one_type.strip())
        types = set(right_types)
        return types


