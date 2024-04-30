from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from aiogram_dialog import DialogManager

import src.keyboards.default.reply as kb
import src.states.user as user_states
from src.data.config import SUPPORT_ID
from src.bot import bot

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
@help_router.message(F.text == 'Назад', StateFilter(user_states.UserFSM.write_message))
async def help_cmd(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await message.answer(help_text, reply_markup=kb.help_kb)
    await state.set_state(user_states.UserFSM.help_menu)


@help_router.message(F.text == 'Позвонить', StateFilter(user_states.UserFSM.help_menu))
async def help_cmd(message: types.Message):
    await message.answer('Телефон горячей линии: +7xxxxxxxxxx', reply_markup=kb.help_kb)


@help_router.message(F.text == 'Написать', StateFilter(user_states.UserFSM.help_menu))
async def help_cmd(message: types.Message, state: FSMContext):
    await message.answer('Напишите ваше сообщение:', reply_markup=kb.back_kb)
    await state.set_state(user_states.UserFSM.write_message)


@help_router.message(StateFilter(user_states.UserFSM.write_message))
async def help_cmd(message: types.Message, state: FSMContext):
    await message.answer('Ваше сообщение отправлено', reply_markup=kb.help_kb)

    await bot.send_message(SUPPORT_ID, f"Новое сообщение от пользователя @{message.from_user.username}: {message.text}")
    await state.set_state(user_states.UserFSM.help_menu)


@help_router.message(F.text == 'Помощь на сайте', StateFilter(user_states.UserFSM.help_menu))
async def help_cmd(message: types.Message):
    await message.answer('Подробная справка на сайте: <ссылка>', reply_markup=kb.help_kb)
