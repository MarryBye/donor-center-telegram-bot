from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    enter_name = State()
    enter_birthDay = State()
    enter_birthMonth = State()
    enter_birthYear = State()
    enter_blood = State()


class Feedback(StatesGroup):
    phone = State()
    mail = State()
    name = State()
