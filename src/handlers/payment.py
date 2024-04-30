from aiogram import Router, types, F

from aiogram_dialog import DialogManager

from src.data.config import PAYMENTS_TOKEN
from src.bot import bot
import src.database.requests as rq
from src.keyboards.inline.payment_method import payment_kb, product_availability
from src.data.config import MANAGER_ID
import src.states.user as user_states
from aiogram.fsm.context import FSMContext

payment_router = Router()


@payment_router.callback_query(F.data == 'to_payment')
async def choose_payment_method(callback: types.CallbackQuery, state: FSMContext, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await callback.message.delete()
    await bot.send_message(MANAGER_ID,
                               f"Новый заказ от пользователя @{callback.from_user.username} на сумму {await rq.get_order_price(callback.from_user.id)} руб.:\n" +
                               "\n".join([(await rq.get_product(cart.product_id)).name for cart in
                                          await rq.orm_get_user_carts(callback.from_user.id)]),
                               reply_markup=product_availability)
    await callback.message.answer("Ваш заказ обработан и передан менеджеру для проверки наличия товара на складе")
    await state.update_data(user_chat_id=callback.message.chat.id)


@payment_router.callback_query(F.data == 'available')
async def process_product_in_stock(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await bot.send_message(user_data['user_chat_id'], "Хорошие новости, товар есть в наличии\nВыберите способ оплаты:", reply_markup=payment_kb)


@payment_router.callback_query(F.data == 'unavailable')
async def process_product_out_of_stock(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await bot.send_message(user_data['user_chat_id'], "К сожалению, в данный момент товара нет в наличии")


@payment_router.callback_query(F.data == 'cash')
async def buy_by_cash(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Ваш заказ оформлен")
    await rq.orm_update_status(callback.from_user.id, 'shop', 'in_progress')


@payment_router.callback_query(F.data == 'card')
async def buy_by_card(callback: types.CallbackQuery):
    await callback.message.delete()
    if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(callback.message.chat.id, "Тестовый платеж!!!")
    await bot.send_invoice(callback.message.chat.id,
                           title="Оформление заказа",
                           description="Оплата заказа",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           is_flexible=False,
                           prices=[types.LabeledPrice(label="Сумма заказа", amount=int((await rq.get_order_price(callback.from_user.id)))*100)],
                           start_parameter="conditioner_payment",
                           payload="invoice-payload")


@payment_router.pre_checkout_query(lambda query: True)
async def process_pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@payment_router.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    await message.answer(f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")
    await message.answer("Ваш заказ оформлен и оплачен")
    await rq.orm_update_payment_status(message.from_user.id)
    await rq.orm_update_status(message.from_user.id, 'shop', 'in_progress')
