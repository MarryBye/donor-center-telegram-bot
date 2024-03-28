from aiogram.fsm.state import State, StatesGroup

class RegisterForm(StatesGroup):
    enter_name = State()
    enter_birthdate = State()
    enter_blood = State()