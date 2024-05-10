from random import choice

from aiogram import Router
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.classes.CRMBot import CRMBot
from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import Form

from src.funcs.core import pressed_button, message_translate, language_name_to_id

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="DONATION ROUTER")


@router.message(pressed_button(button_name="DONATION_MENU_REGISTER"))
async def main_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    db.register_donor_appointment(user_id=user_id, clinic_id=1, registration_date="18-09-2004",
                                  appointment_date="19-09-2004")

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.DONATION, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="DONATION_REGISTERED_APPOINTMENT", language_name=user_language)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


@router.message(pressed_button(button_name="DONATION_MENU_FIND_CENTER"))
async def main_handler(msg: Message):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    clinics_text = "\n".join([str(clinic[0]) for clinic in db.get_clinics()])

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.DONATION, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="DONATION_FIND_CENTERS_MESSAGE", language_name=user_language) % (
        msg.from_user.username, clinics_text)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


@router.message(pressed_button(button_name="DONATION_MENU_HISTORY"))
async def main_handler(msg: Message):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    all_appointments = db.get_donor_appointments(user_id=user_id)

    history_text = ""
    quantity_appointments = 0

    if all_appointments:
        for appointment in db.get_donor_appointments(user_id=user_id):
            history_text += f"{appointment[0]}: центр {appointment[1]}, статус: {appointment[3]}\n"
        quantity_appointments = len(all_appointments)

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.DONATION, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="DONATION_HISTORY_MESSAGE", language_name=user_language) % (
        msg.from_user.username, quantity_appointments, history_text)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


hnd.add_router(router)
