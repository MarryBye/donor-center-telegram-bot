from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    sendContact = State()
    registerUser_language = State()
    registerUser_contact = State()
    registerUser_birthday = State()
    registerUser_password = State()
    registerUser_gender = State()
    registerUser_email = State()


class Feedback(StatesGroup):
    phone = State()
    mail = State()
    name = State()
