from aiogram import Router, types, F
from src.data.config import PAYMENTS_TOKEN
from src.bot import bot
import src.database.requests as rq
from src.keyboards.inline.payment_method import payment_kb
from src.data.config import SUPPORT_ID

payment_router = Router()


async def get_order_price(tg_id):
    data = await rq.orm_get_user_carts(tg_id)
    order_price = 0
    for order in data:
        prod = await rq.get_product(order.product_id)
        order_price += prod.price
    return int(order_price * 100)


@payment_router.callback_query(F.data == 'to_payment')
async def choose_payment_method(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Выберите способ оплаты:", reply_markup=payment_kb)


@payment_router.callback_query(F.data == 'cash')
async def buy_by_cash(callback: types.CallbackQuery):
    await callback.message.delete()
    await bot.send_message(SUPPORT_ID, f"Новый заказ от пользователя @{callback.from_user.username} на сумму {await get_order_price(callback.from_user.id)}: "
                                       f"{[(await rq.get_product(cart.product_id)).name for cart in await rq.orm_get_user_carts(callback.from_user.id)]}")
    await callback.message.answer("Ваш заказ обработан и передан менеджеру, ожидайте дальнейшей связи")
    await rq.orm_update_status(callback.from_user.id, 'shop', 'in_progress')


@payment_router.callback_query(F.data == 'card')
async def buy_by_card(callback: types.CallbackQuery):
    if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(callback.message.chat.id, "Тестовый платеж!!!")
    await bot.send_invoice(callback.message.chat.id,
                           title="Оформление заказа",
                           description="Оплата заказа",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           is_flexible=False,
                           prices=[types.LabeledPrice(label="Сумма заказа", amount=await get_order_price(callback.from_user.id))],
                           start_parameter="conditioner_payment",
                           payload="test-invoice-payload")


@payment_router.pre_checkout_query(lambda query: True)
async def process_pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@payment_router.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    await message.answer(f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")
    await rq.orm_update_status(message.from_user.id, 'shop', 'in_progress')
