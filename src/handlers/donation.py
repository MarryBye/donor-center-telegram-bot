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
from datetime import datetime, timedelta

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

    if last_appointment is not None and last_appointment.get_status().get_name_status() == "Waiting":

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

        if str(clinic_region.get_id()) == data["region_id"] and str(clinic_city.get_id()) == data["city_id"]:
            regional_clinics.append(clinic)

    if len(regional_clinics) == 0:
        state.clear()
        await bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            reply_markup=None
        )

        await bot.answer(
            user_id=user_id,
            text="DONATION_SELECT_CLINIC",
            keyboard_name=KeyboardName.DONATION,
            keyboard_type=KeyboardType.REPLY,
            language_name=user_language
        )

        return False

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

    register_date = datetime.now()
    appointment_date = register_date + timedelta(days=7)

    new_appointment = Appointment()
    new_appointment.set_id(db.get_next_row_id("data_blood.appointment"))
    new_appointment.set_clinic(clinic=clinic)
    new_appointment.set_status(status=db.get_status(status_id=3))
    new_appointment.set_donor(donor=donor)
    new_appointment.set_registration_date(registration_date=register_date)
    new_appointment.set_appointment_date(appointment_date=appointment_date)
    new_appointment.set_analysis_file_path(analysis_file_path=f"{donor.get_id()}%{clinic.get_id()}%{register_date.day}{register_date.month}{register_date.year}.txt")

    db.register_appointment(donor=donor, appointment=new_appointment)

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

    clinics = [clinic for clinic in db.get_clinics()]

    clinics_text = ""

    for clinic in clinics:
        address = clinic.get_address()
        region = address.get_region().get_region_name()
        city = address.get_city().get_city_name()
        street = address.get_street().get_street_name()
        area = address.get_area().get_area_name()
        house = address.get_house_number()
        clinics_text += f"#{clinic.get_id()}: {clinic.get_clinic_name()}\nАдреса: м. {city}, {region}, вул. {street}, площа {area}, будинок №{house}\n\n"

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.DONATION, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="DONATION_FIND_CENTERS_MESSAGE", language_name=user_language) % (
        msg.from_user.username, clinics_text)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


@router.message(pressed_button(button_name="DONATION_MENU_HISTORY"))
async def main_handler(msg: Message):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    donor = db.get_donor(telegram_id=user_id)
    all_appointments = db.get_donor_appointment(donor=donor, only_last=False)

    history_text = ""
    quantity_appointments = 0

    if all_appointments:
        for appointment in all_appointments:
            clinic = appointment.get_clinic()
            address = clinic.get_address()
            region = address.get_region().get_region_name()
            city = address.get_city().get_city_name()
            street = address.get_street().get_street_name()
            area = address.get_area().get_area_name()
            house = address.get_house_number()
            clinic_name = clinic.get_clinic_name()
            status_name = appointment.get_status().get_name_status()
            registration_date = appointment.get_registration_date()
            appointment_date = appointment.get_appointment_date()
            history_text += f"№{appointment.get_id()}\nДата реєстрації: {registration_date}\nДата прийому: {appointment_date}\nЦентр: '{clinic_name}, Адреса: м. {city}, {region}, вул. {street}, площа {area}, будинок №{house}'\nСтатус: {status_name}\n\n"
        quantity_appointments = len(all_appointments)

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.DONATION, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="DONATION_HISTORY_MESSAGE", language_name=user_language) % (
        msg.from_user.username, quantity_appointments, history_text)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


hnd.add_router(router)
