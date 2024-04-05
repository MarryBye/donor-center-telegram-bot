from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    sendContact = State()


class Feedback(StatesGroup):
    phone = State()
    mail = State()
    name = State()
