import datetime

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.classes.CRMBot import CRMBot
from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.Controllers.DonorsDatabaseController import DonorsDatabaseController
from src.classes.Controllers.AppointmentsDatabaseController import AppointmentsDatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType, Keyboard
from src.classes.Form import FormAppointment
from src.classes.Datatypes.Appointment import Appointment
from datetime import datetime

from src.funcs.core import pressed_button, message_translate

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

    donor = db.get_donor(telegram_id=user_id)
    last_appointment = db.get_donor_appointment(donor=donor, only_last=True)

    if last_appointment is None or last_appointment.get_status().get_name_status() == "Waiting":

        await bot.answer(
            user_id=user_id,
            text="CANNOT_REGISTER",
            keyboard_name=KeyboardName.DONATION,
            keyboard_type=KeyboardType.REPLY,
            language_name=user_language
        )

        return False

    await state.update_data(donor=donor)
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

    all_clinics = db.get_clinics()
    regional_clinics = []

    for clinic in all_clinics:
        clinic_address = clinic.get_address()
        clinic_region, clinic_city = clinic_address.get_region(), clinic_address.get_city()

        if clinic_region.get_id() == data["region_id"] and clinic_city.get_id() == data["city_id"]:
            regional_clinics.append(clinic)

    kb_scheme = []
    kb_scheme_row = []
    for i, clinic in enumerate(regional_clinics, start=0):
        kb_scheme_row.append({clinic.get_clinic_name(): {"callback_data": str(clinic.get_id())}})
        if i % 3 == 0 or i >= len(regional_clinics) - 1:
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

    data = await state.get_data()

    clinic = db.get_clinic(clinic_id=call.data)
    donor = data["donor"]

    date = datetime.now()

    new_appointment = Appointment()
    new_appointment.set_id(db.get_next_row_id("data_blood.appointment"))
    new_appointment.set_clinic(clinic=clinic)
    new_appointment.set_status(status=db.get_status(status_id=3))
    new_appointment.set_donor(donor=donor)
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
            history_text += f"{appointment.get_id()}: центр {appointment.get_clinic_id()}, статус: {appointment.get_status()}\n"
        quantity_appointments = len(all_appointments)

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.DONATION, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="DONATION_HISTORY_MESSAGE", language_name=user_language) % (
        msg.from_user.username, quantity_appointments, history_text)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


hnd.add_router(router)
