from aiogram.fsm.state import State, StatesGroup


class UserFSM(StatesGroup):
    help_menu = State()
    settings_menu = State()
    write_message = State()
    write_name = State()
    write_phone = State()
    rewrite_name = State()
    rewrite_phone = State()

    write_price = State()
    choosing_control_type = State()
    choosing_appointment_type = State()


