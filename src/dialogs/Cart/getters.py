from src.database.models import async_session, Cart, Catalog
from sqlalchemy import select
from src.utils.funcs import get_image_size, get_image_ratio
from src.database.requests import get_order_price
from aiogram_dialog import DialogManager



#получение товаров в корзине
async def get_products(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        db_main = set(await session.scalars(select(Cart.product_id).where(Cart.tg_id == dialog_manager.current_context().start_data.get('user_id'), Cart.status == 'shop')))

        data = {
            'products': [(item, await session.scalar(select(Catalog.name).where(Catalog.id == item))) for item in db_main],
            'total_price': await get_order_price(dialog_manager.current_context().start_data.get('user_id'))
        }
        return data

async def get_item(dialog_manager: DialogManager, **middleware_data):
     async with async_session() as session:
        db_main = await session.scalar(select(Catalog).where(Catalog.id == int(dialog_manager.current_context().dialog_data.get('product_id'))))
        db_quantity = await session.scalar(select(Cart.quantity).where(Cart.product_id == int(dialog_manager.current_context().dialog_data.get('product_id'))))
        if db_main.image == '':
            image = 'https://cdn-icons-png.flaticon.com/512/4054/4054617.png'
        else:
            size = await get_image_size(db_main.image)
            ratio = await get_image_ratio(db_main.image)
            if (size and size > 10) or (ratio[0] and ratio[0] + ratio[1] > 10000 or ratio[2] > 20):
                image = 'https://cdn-icons-png.flaticon.com/512/4054/4054617.png'
            else:
                image = db_main.image

        price = f'{float(db_main.price) * 0.85} скидка ({float(db_main.price) - (float(db_main.price) * 0.85)}) Руб.'
        total_price_card = f'{float(db_main.price) * 0.85 * float(db_quantity)} Руб.'
        data = {'name': db_main.name,
                'image': image,
                'price': price,
                'quantity': db_quantity,
                'total_price_card': total_price_card
                }

        return data
