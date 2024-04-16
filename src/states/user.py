from aiogram.fsm.state import State, StatesGroup


class UserFSM(StatesGroup):
    write_message = State()
    write_name = State()
    write_phone = State()
    rewrite_name = State()
    rewrite_phone = State()
