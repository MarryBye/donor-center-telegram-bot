from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    sendContact = State()
    registerUser_language = State()
    registerUser_contact = State()
    registerUser_birthday = State()
    registerUser_password = State()
    registerUser_gender = State()
    registerUser_email = State()


class ChooseLanguage(StatesGroup):
    choose_language = State()


class ChooseNotifications(StatesGroup):
    choose_notification = State()


class FormAppointment(StatesGroup):
    registerAppointment_city = State()
    registerAppointment_region = State()
    registerAppointment_clinic = State()
    registerAppointment_date = State()


class Feedback(StatesGroup):
    phone = State()
    mail = State()
    name = State()


class UserSettings(StatesGroup):
    name = State()
    number = State()
    bdate = State()
    gender = State()
    email = State()
