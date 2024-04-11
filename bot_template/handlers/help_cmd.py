from aiogram import types, Router, F
from aiogram.filters import Command
import bot_template.keyboards.reply as kb

help_router = Router()

help_text = """
Список команд:
/catalog - Каталог
/cart — Корзина
/history — История заказов
/settings — Настройки
/help — Справка
/start — Главное меню
/delivery — Информация о доставке
/news — Новости
        
Ответы на часто задаваемые вопросы:

"""


@help_router.message(Command(commands='help'))
@help_router.message(F.text == 'Помощь')
@help_router.message(F.text == 'Назад')
async def help_cmd(message: types.Message):
    await message.answer(help_text, reply_markup=kb.help_kb)


@help_router.message(F.text == 'Позвонить')
async def help_cmd(message: types.Message):
    await message.answer('Телефон горячей линии: +7xxxxxxxxxx', reply_markup=kb.help_kb)


@help_router.message(F.text == 'Написать')
async def help_cmd(message: types.Message):
    await message.answer('Напишите ваше сообщение:', reply_markup=kb.back_kb)


@help_router.message(F.text == 'Помощь на сайте')
async def help_cmd(message: types.Message):
    await message.answer('Подробная справка на сайте: <ссылка>', reply_markup=kb.help_kb)
