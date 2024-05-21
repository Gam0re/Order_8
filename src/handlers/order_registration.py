from aiogram import Router, types, F

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from src.bot import bot
import src.database.requests as rq


from src.data.config import MANAGER_ID
from src.handlers.registration import start_registration_name
from src.keyboards.inline.order_registration_kb import product_availability

order_registration_router = Router()


#@order_registration_router.callback_query(F.data == 'agree')
async def checking_phone_number(callback: types.CallbackQuery, widget: Button, dialog_manager: DialogManager):
    state = dialog_manager.middleware_data.get('state')
    try:
        await dialog_manager.done()
    except:
        pass
    phone = await rq.get_number(callback.from_user.id)
    if not phone:
        await callback.message.delete()
        await state.update_data(from_settings_registration=False)
        await start_registration_name(callback.message, state)
    else:
        await checking_product_availability(callback)


@order_registration_router.callback_query(F.data == 'continue')
async def checking_product_availability(callback: types.CallbackQuery):
    await callback.message.delete()
    await bot.send_message(MANAGER_ID,
                           f"Новый заказ от пользователя @{callback.from_user.username} на имя: {await rq.get_name(callback.from_user.id)} Номер телефона: {await rq.get_number(callback.from_user.id)} User id: {callback.from_user.id} Сумма заказа: {await rq.get_order_price(callback.from_user.id)} руб.:\n" +
                           "\n".join([(await rq.get_product(cart.product_id)).name for cart in
                                      await rq.orm_get_user_carts(callback.from_user.id)]),
                           reply_markup=product_availability)
    await callback.message.answer("Ваш заказ обработан и передан менеджеру для проверки наличия товара на складе")


@order_registration_router.callback_query(F.data == 'available')
async def process_product_in_stock(callback: types.CallbackQuery):
    user_id = int(callback.message.text[callback.message.text.find('User id:') + 9:callback.message.text.find(' Сумма заказа:')])
    await bot.send_message(user_id, "Хорошие новости, товар есть в наличии\nОжидайте дальнейшей связи с менеджером")
    await rq.orm_update_status(user_id, 'shop', 'in_progress')
    await callback.message.edit_text(callback.message.text + "\nВЫ ОТВЕТИЛИ НА ЭТУ ЗАЯВКУ, ЧТО ТОВАР ЕСТЬ В НАЛИЧИИ")


@order_registration_router.callback_query(F.data == 'unavailable')
async def process_product_out_of_stock(callback: types.CallbackQuery):
    user_id = int(callback.message.text[callback.message.text.find('User id:') + 9:callback.message.text.find(' Сумма заказа:')])
    await bot.send_message(user_id, "К сожалению, в данный момент товара нет в наличии")
    await callback.message.edit_text(callback.message.text + "\nВЫ ОТВЕТИЛИ НА ЭТУ ЗАЯВКУ, ЧТО ТОВАРА НЕТ В НАЛИЧИИ")
