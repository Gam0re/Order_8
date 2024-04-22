from aiogram.fsm.state import State, StatesGroup

class Catalog_levels(StatesGroup):
    level_1 = State()
    level_2 = State()
    level_3 = State()
    level_4 = State()
    level_5 = State()
    item = State()
    select_item = State()
