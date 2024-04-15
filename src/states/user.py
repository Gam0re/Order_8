from aiogram.fsm.state import State, StatesGroup


class UserFSM(StatesGroup):
    write_message = State()
