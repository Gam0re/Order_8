from aiogram import types, Router, F

from aiogram.filters import Command
from aiogram.types import InputMediaPhoto

from aiogram_dialog import DialogManager

from src.keyboards.inline.cart import cart_kb
import src.database.requests as rq

cart_router = Router()

cart_config = ... #тут подгрузить bot_config.json["texts"]["cart"]

# корзина
@cart_router.message(Command(cart_config['command']))
@cart_router.message(F.text == cart_config['reply_button'])
async def get_carts(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.done()
    data = await rq.orm_get_user_carts(message.from_user.id)
    order_price = await rq.get_order_price(message.from_user.id)
    if len(data) > 0:
        page = 0
        media = await rq.orm_get_user_media(message.from_user.id, data[page].product_id, page+1, len(data))
        await message.answer_photo(photo=media['photo'], caption=media['name'], reply_markup=cart_kb(page, order_price))
    else:
        await message.answer(text=cart_config['empty'])

@cart_router.callback_query(F.data.startswith('next_'))
async def get_carts_next(callback: types.CallbackQuery):
    data = await rq.orm_get_user_carts(callback.from_user.id)
    page = int(callback.data.split('_')[1]) + 1
    order_price = await rq.get_order_price(callback.from_user.id)
    if len(data) >= page + 1:
        await callback.answer(cart_config['next_page'])
        media = await rq.orm_get_user_media(callback.from_user.id, data[page].product_id, page+1, len(data))
        await callback.message.edit_media(media=InputMediaPhoto(media=media['photo'], caption=media['name']), reply_markup=cart_kb(page, order_price))
    else:
        await callback.answer(cart_config['no_pages'])

@cart_router.callback_query(F.data.startswith('back_'))
async def get_carts_back(callback: types.CallbackQuery):
    data = await rq.orm_get_user_carts(callback.from_user.id)
    page = int(callback.data.split('_')[1]) - 1
    order_price = await rq.get_order_price(callback.from_user.id)
    if len(data) >= page + 1 and page >= 0:
        await callback.answer(cart_config['back_page'])
        media = await rq.orm_get_user_media(callback.from_user.id, data[page].product_id, page+1, len(data))
        await callback.message.edit_media(media=InputMediaPhoto(media=media['photo'], caption=media['name']), reply_markup=cart_kb(page, order_price))
    else:
        await callback.answer(cart_config['first_page'])

@cart_router.callback_query(F.data.startswith('decrement_'))
async def get_carts_decrement(callback: types.CallbackQuery):
    data = await rq.orm_get_user_carts(callback.from_user.id)
    page = int(callback.data.split('_')[1])
    delete = await rq.orm_reduce_product_in_cart(callback.from_user.id, data[page].product_id)
    data_sec = await rq.orm_get_user_carts(callback.from_user.id)
    order_price = await rq.get_order_price(callback.from_user.id)
    if delete:
        await callback.answer(cart_config['out_item'])
        media = await rq.orm_get_user_media(callback.from_user.id, data_sec[page].product_id, page+1, len(data_sec))
        await callback.message.edit_media(media=InputMediaPhoto(media=media['photo'], caption=media['name']), reply_markup=cart_kb(page, order_price))
    else:
        await callback.answer(cart_config['deleted_item'])
        page = 0
        if len(data_sec) >= 1:
            media = await rq.orm_get_user_media(callback.from_user.id, data_sec[page].product_id, page+1, len(data_sec))
            await callback.message.edit_media(media=InputMediaPhoto(media=media['photo'], caption=media['name']), reply_markup=cart_kb(page, order_price))
        else:
            await callback.message.delete()
            await callback.message.answer(text=cart_config['empty'])

@cart_router.callback_query(F.data.startswith('increment_'))
async def get_carts_increment(callback: types.CallbackQuery):
    data = await rq.orm_get_user_carts(callback.from_user.id)
    await callback.answer(cart_config['added_item'])
    page = int(callback.data.split('_')[1])
    await rq.orm_add_to_cart(callback.from_user.id, data[page].product_id)
    data_sec = await rq.orm_get_user_carts(callback.from_user.id)
    order_price = await rq.get_order_price(callback.from_user.id)
    media = await rq.orm_get_user_media(callback.from_user.id, data_sec[page].product_id, page+1, len(data_sec))
    await callback.message.edit_media(media=InputMediaPhoto(media=media['photo'], caption=media['name']), reply_markup=cart_kb(page, order_price))

@cart_router.callback_query(F.data.startswith('delete_'))
async def get_carts_delete(callback: types.CallbackQuery):
    data = await rq.orm_get_user_carts(callback.from_user.id)
    await callback.answer(cart_config['deleted_item'])
    page = int(callback.data.split('_')[1])
    await rq.orm_delete_from_cart(callback.from_user.id, data[page].product_id)
    data_sec = await rq.orm_get_user_carts(callback.from_user.id)
    order_price = await rq.get_order_price(callback.from_user.id)
    page = 0
    if len(data_sec) >= 1:
        media = await rq.orm_get_user_media(callback.from_user.id, data_sec[page].product_id, page+1, len(data_sec))
        await callback.message.edit_media(media=InputMediaPhoto(media=media['photo'], caption=media['name']), reply_markup=cart_kb(page, order_price))
    else:
        await callback.message.delete()
        await callback.message.answer(text=cart_config['empty'])
