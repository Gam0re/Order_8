from aiogram.fsm.state import State, StatesGroup

class dialogFSM(StatesGroup):
    level1 = State()
    level2 = State()
    level3 = State()
    level4 = State()
    level5 = State()
    first_level_state = State()
class choosingFSM(StatesGroup):
    choose = State()

class buyFSM(StatesGroup):
    enter_amount = State()
    confirm = State()