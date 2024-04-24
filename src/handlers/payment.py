from aiogram import Router, types, F
from src.data.config import PAYMENTS_TOKEN
from src.bot import bot
import src.database.requests as rq

payment_router = Router()


@payment_router.callback_query(F.data == 'to_payment')
async def buy(callback: types.CallbackQuery):
    if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(callback.message.chat.id, "Тестовый платеж!!!")
    await bot.send_invoice(callback.message.chat.id,
                           title="Оформление заказа",
                           description="Оплата заказа",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           is_flexible=False,
                           prices=[types.LabeledPrice(label="Сумма заказа", amount=await rq.get_order_price(callback.from_user.id))],
                           start_parameter="conditioner_payment",
                           payload="test-invoice-payload")


@payment_router.pre_checkout_query(lambda query: True)
async def process_pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@payment_router.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    await message.answer(f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")
    await rq.orm_update_status(message.from_user.id, 'shop', 'in_progress')
