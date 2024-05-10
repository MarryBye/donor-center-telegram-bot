from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    sendContact = State()
    registerUser_contact = State()
    registerUser_birthday = State()
    registerUser_password = State()
    registerUser_gender = State()


class Feedback(StatesGroup):
    phone = State()
    mail = State()
    name = State()
