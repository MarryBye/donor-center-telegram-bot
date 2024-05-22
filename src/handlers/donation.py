import datetime
from random import choice

from aiogram import Router
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.classes.CRMBot import CRMBot
from src.classes.DatabaseController import DatabaseController, DonorsDatabaseController, AppointmentsDatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType, Keyboard
from src.classes.Form import FormAppointment
from src.classes.Appointment import Appointment
from datetime import datetime

from src.funcs.core import pressed_button, message_translate, language_name_to_id, sent_callback

bot = CRMBot()

db = DatabaseController()
db_donors = DonorsDatabaseController()
db_appointments = AppointmentsDatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="DONATION ROUTER")


@router.message(pressed_button(button_name="DONATION_MENU_REGISTER"))
async def main_handler(msg: Message, state: FSMContext):

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    donor = db_donors.get_donor_by(telegram_id=user_id)

    if not db_appointments.get_donor_appointments(donor=donor, need_status=3, only_last=True).is_empty():

        await bot.answer(
            user_id=user_id,
            text="CANNOT_REGISTER",
            keyboard_name=KeyboardName.DONATION,
            keyboard_type=KeyboardType.REPLY,
            language_name=user_language
        )

        return False

    await state.set_state(FormAppointment.registerAppointment_city)

    await bot.answer(
        user_id=user_id,
        text="DONATION_SELECT_CITY",
        keyboard_name=KeyboardName.CITIES,
        keyboard_type=KeyboardType.INLINE,
        language_name=user_language
    )


@router.callback_query(FormAppointment.registerAppointment_city)
async def main_handler(call: CallbackQuery, state: FSMContext):

    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    await state.update_data(city_id=call.data)
    await state.set_state(FormAppointment.registerAppointment_region)

    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    await bot.answer(
        user_id=user_id,
        text="DONATION_SELECT_REGION",
        keyboard_name=KeyboardName.REGIONS,
        keyboard_type=KeyboardType.INLINE,
        language_name=user_language
    )


@router.callback_query(FormAppointment.registerAppointment_region)
async def main_handler(call: CallbackQuery, state: FSMContext):

    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    await state.update_data(region_id=call.data)
    await state.set_state(FormAppointment.registerAppointment_clinic)

    data = await state.get_data()

    clinics = db.get_clinics_by(city=data["city_id"], region=data["region_id"])

    kb_scheme = []
    kb_scheme_row = []
    for i, clinic in enumerate(clinics, start=0):
        kb_scheme_row.append({clinic["clinic_name"]: {"callback_data": str(clinic["ID"])}})
        if i % 3 == 0 or i >= len(clinics) - 1:
            kb_scheme.append(kb_scheme_row)
            kb_scheme_row = []

    keyboard = Keyboard(keyboard_scheme=kb_scheme, need_translation=False)

    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    await bot.answer(
        user_id=user_id,
        text="DONATION_SELECT_CLINIC",
        keyboard_name=keyboard,
        keyboard_type=KeyboardType.INLINE,
        language_name=user_language
    )


@router.callback_query(FormAppointment.registerAppointment_clinic)
async def main_handler(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    clinic = db.get_clinics_by(db_id=int(call.data))[0]
    donor = db_donors.get_donor_by(telegram_id=user_id)
    date = datetime.now()

    new_appointment = Appointment()
    new_appointment.set_id(db.get_next_row_id("data_blood.appointment"))
    new_appointment.set_clinic_id(clinic_id=clinic["ID"])
    new_appointment.set_status_id(status_id=3)
    new_appointment.set_donor_number_id(donor_number_id=donor.get_number_id())
    new_appointment.set_registration_date(f"{date.day}-{date.month}-{date.year}")
    new_appointment.set_appointment_date(appointment_date="19-05-2024")
    new_appointment.set_analysis_file_path(analysis_file_path=f"{donor.get_id()}%{clinic['ID']}%{date.day}{date.month}{date.year}.txt")

    db_appointments.register_donor_appointment(donor=donor, appointment=new_appointment)

    await state.clear()

    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    await bot.answer(
        user_id=user_id,
        text="DONATION_REGISTERED_APPOINTMENT",
        keyboard_name=KeyboardName.DONATION,
        keyboard_type=KeyboardType.REPLY,
        language_name=user_language
    )


@router.message(pressed_button(button_name="DONATION_MENU_FIND_CENTER"))
async def main_handler(msg: Message):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    clinics_text = "\n".join([" - ".join(list(map(str, clinic.values()))) for clinic in db.get_clinics()])

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.DONATION, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="DONATION_FIND_CENTERS_MESSAGE", language_name=user_language) % (
        msg.from_user.username, clinics_text)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


@router.message(pressed_button(button_name="DONATION_MENU_HISTORY"))
async def main_handler(msg: Message):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    donor = db_donors.get_donor_by(telegram_id=user_id)
    all_appointments = db_appointments.get_donor_appointments(donor=donor, only_last=False)

    history_text = ""
    quantity_appointments = 0

    if all_appointments:
        for appointment in all_appointments:
            history_text += f"{appointment.get_id()}: центр {appointment.get_clinic_id()}, статус: {appointment.get_status_id()}\n"
        quantity_appointments = len(all_appointments)

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.DONATION, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="DONATION_HISTORY_MESSAGE", language_name=user_language) % (
        msg.from_user.username, quantity_appointments, history_text)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


hnd.add_router(router)
