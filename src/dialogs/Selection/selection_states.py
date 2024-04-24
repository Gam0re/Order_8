from aiogram.fsm.state import State, StatesGroup

class SelectionStates(StatesGroup):
    searching_products = State()
    view_product = State()
