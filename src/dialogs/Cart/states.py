from aiogram.fsm.state import State, StatesGroup

class Cart_levels(StatesGroup):
    select_products = State()
    product_card = State()
