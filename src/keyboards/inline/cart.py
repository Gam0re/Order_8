from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class MenuCallBack(CallbackData, prefix="menu"):
    menu_name: str
    page: int = 1
    product_id: int


def get_user_cart(
    *,
    page: int,
    pagination_btns: dict,
    product_id: int,
):
    keyboard = InlineKeyboardBuilder()
    if page != 0:
        keyboard.add(InlineKeyboardButton(text='Удалить',
                    callback_data=MenuCallBack(menu_name='delete', product_id=product_id, page=page).pack()))
        keyboard.add(InlineKeyboardButton(text='-1',
                    callback_data=MenuCallBack(menu_name='decrement', product_id=product_id, page=page).pack()))
        keyboard.add(InlineKeyboardButton(text='+1',
                    callback_data=MenuCallBack(menu_name='increment', product_id=product_id, page=page).pack()))

        keyboard.adjust(3)

        row = []
        for text, menu_name in pagination_btns.items():
            if menu_name == "next":
                row.append(InlineKeyboardButton(text=text,
                        callback_data=MenuCallBack(menu_name=menu_name, page=page + 1).pack()))
            elif menu_name == "previous":
                row.append(InlineKeyboardButton(text=text,
                        callback_data=MenuCallBack(menu_name=menu_name, page=page - 1).pack()))

        keyboard.row(*row)

        row2 = [
        InlineKeyboardButton(text='На главную 🏠',
                    callback_data=MenuCallBack(menu_name='to_main').pack()),
        InlineKeyboardButton(text='Заказать',
                    callback_data=MenuCallBack(menu_name='order').pack()),
        ]
        return keyboard.row(*row2).as_markup()
    else:
        keyboard.add(
            InlineKeyboardButton(text='На главную 🏠',
                    callback_data=MenuCallBack(menu_name='to_main').pack()))

        return keyboard.adjust(3).as_markup()
