from aiogram import types, Router, F

from aiogram.filters import Command
from aiogram.types import InputMediaPhoto, InputTextMessageContent
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.requests import orm_add_to_cart
from src.keyboards.inline.cart import MenuCallBack, get_user_cart
import src.database.requests as rq
from src.database.models import Catalog
from src.utils.Paginator import Paginator
from sqlalchemy import select

cart_router = Router()

def pages(paginator: Paginator):
    btns = dict()
    if paginator.has_previous():
        btns["◀ Пред."] = "previous"

    if paginator.has_next():
        btns["След. ▶"] = "next"

    return btns

async def carts(session, menu_name, page, user_id, product_id):
    if menu_name == "delete":
        await rq.orm_delete_from_cart(session, user_id, product_id)
        if page > 1:
            page -= 1
    elif menu_name == "decrement":
        is_cart = await rq.orm_reduce_product_in_cart(session, user_id, product_id)
        if page > 1 and not is_cart:
            page -= 1
    elif menu_name == "increment":
        await orm_add_to_cart(session, user_id, product_id)

    carts = await rq.orm_get_user_carts(session, user_id)

    if not carts:
        image = InputTextMessageContent(message_text='У вас нет товаров в корзине')
        kbds = get_user_cart(
            page=0,
            pagination_btns={0:0},
            product_id=0,
        )

    else:
        paginator = Paginator(carts, page=page)

        cart = paginator.get_page()[0]

        image = InputMediaPhoto(
            media=await session.scalars(select(Catalog.image).where(Catalog.id == product_id)),
            caption=f"<strong>{cart.product.name}</strong>\
                    \nТовар {paginator.page} из {paginator.pages} в корзине.\nОбщая стоимость товаров в корзине:",
        )

        pagination_btns = pages(paginator)

        kbds = get_user_cart(
            page=page,
            pagination_btns=pagination_btns,
            product_id=cart.product.id,
        )

    return image, kbds


# корзина
@cart_router.message(Command('cart'))
@cart_router.message(F.text == 'Корзина')
async def get_carts(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):

    media, reply_markup = await carts(
        session=session,
        menu_name=callback_data.menu_name,
        page=callback_data.page,
        product_id=callback_data.product_id,
        user_id=callback.from_user.id,
    )
    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()
