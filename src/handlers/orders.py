from aiogram import types, Router, F

from aiogram.filters import Command

from aiogram_dialog import DialogManager

import src.keyboards.inline.order as kb
import src.database.requests as rq

order_router = Router()


# команда заказы
@order_router.message(Command(commands='orders'))
@order_router.message(F.text == 'Заказы')
@order_router.message(F.data == 'main_orders')
async def start_order(message: types.Message, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await message.answer("Выберите, что вы хотите посмотреть", reply_markup=kb.order_kb)

@order_router.callback_query(F.data == 'in_progress')
async def in_progress(callback: types.CallbackQuery):
    await callback.answer('В процессе')
    text = await rq.get_orders(callback.from_user.id, 'in_progress')
    if text == '':
        await callback.message.edit_text('Ваши товары ещё в обработке, ждите ответ от менеджера', reply_markup=kb.order_back)
    else:
        await callback.message.edit_text(text=f'Отлично! Вы оплатили следующие товары:\n{text}Забрать их можно по адресу:', reply_markup=kb.order_back)

@order_router.callback_query(F.data == 'done')
async def in_progress(callback: types.CallbackQuery):
    await callback.answer('История')
    text = await rq.get_orders(callback.from_user.id, 'done')
    if text == '':
        await callback.message.edit_text('Вы ещё ничего не заказывали', reply_markup=kb.order_back)
    else:
        await callback.message.edit_text(text=f'Товары которые вы уже забрали:\n{text}Спасибо, что выбрали нас!', reply_markup=kb.order_back)

@order_router.callback_query(F.data == 'main_orders')
async def edit_start_order(callback: types.CallbackQuery):
    await callback.answer('Назад')
    await callback.message.edit_text(text="Выберите, что вы хотите посмотреть", reply_markup=kb.order_kb)
