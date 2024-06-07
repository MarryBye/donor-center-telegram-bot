import asyncio

from re import match

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.classes.CRMBot import CRMBot
from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType, Keyboard
from src.classes.Form import FormAdmin, AdminFunc

from src.funcs.core import message_translate, pressed_button, button_translate
from src.funcs.debug_print import debug_print

bot = CRMBot()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="Admin panel router")


@router.message(Command("admin"))
async def main_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    admin = db.get_admin_authenticated(user_id=user_id)

    if admin:

        await bot.answer(
            user_id=user_id,
            text="ADMIN_ALREADY_AUTHENTICATED",
            keyboard_name=KeyboardName.ADMIN,
            keyboard_type=KeyboardType.REPLY,
            language_name=user_language
        )

        return True

    if await state.get_state() is None:
        await state.set_state(FormAdmin.input_login)

        await bot.answer(
            user_id=user_id,
            text="ADMIN_LOGIN",
            language_name=user_language
        )

        await bot.answer(
            user_id=user_id,
            text="ADMIN_INPUT_LOGIN",
            language_name=user_language
        )

        debug_print("User", user_id, "has started login as administator!")


@router.message(FormAdmin.input_login)
async def main_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    if msg.text is None:
        bot_msg = await bot.answer(
            user_id=user_id,
            text="ADMIN_INCORRECT_DATA",
            language_name=user_language
        )

        await asyncio.sleep(5)
        await bot_msg.delete()
        await msg.delete()

        return False

    await state.update_data(login=msg.text)
    await state.set_state(FormAdmin.input_password)

    await bot.answer(
        user_id=user_id,
        text="ADMIN_INPUT_PASSWORD",
        language_name=user_language
    )

    await msg.delete()


@router.message(FormAdmin.input_password)
async def main_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    if msg.text is None:
        bot_msg = await bot.answer(
            user_id=user_id,
            text="ADMIN_INCORRECT_DATA",
            language_name=user_language
        )

        await asyncio.sleep(5)
        await bot_msg.delete()
        await msg.delete()

        return False

    await state.update_data(password=msg.text)
    await state.set_state(FormAdmin.input_city)

    await bot.answer(
        user_id=user_id,
        text="ADMIN_INPUT_CLINIC_CITY",
        keyboard_name=KeyboardName.CITIES,
        keyboard_type=KeyboardType.INLINE,
        language_name=user_language
    )

    await msg.delete()


@router.callback_query(FormAdmin.input_city)
async def main_handler(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    await state.update_data(city_id=call.data)
    await state.set_state(FormAdmin.input_region)

    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    await bot.answer(
        user_id=user_id,
        text="ADMIN_INPUT_CLINIC_REGION",
        keyboard_name=KeyboardName.REGIONS,
        keyboard_type=KeyboardType.INLINE,
        language_name=user_language
    )


@router.callback_query(FormAdmin.input_region)
async def main_handler(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    await state.update_data(region_id=call.data)
    await state.set_state(FormAdmin.input_clinic)

    data = await state.get_data()

    all_clinics = db.get_clinics()
    regional_clinics = []

    for clinic in all_clinics:
        clinic_address = clinic.get_address()
        clinic_region, clinic_city = clinic_address.get_region(), clinic_address.get_city()

        if str(clinic_region.get_id()) == data["region_id"] and str(clinic_city.get_id()) == data["city_id"]:
            regional_clinics.append(clinic)

    if len(regional_clinics) == 0:
        await state.clear()
        await bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            reply_markup=None
        )

        await bot.answer(
            user_id=user_id,
            text="ADMIN_INCORRECT_DATA",
            keyboard_name=KeyboardName.MAIN,
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


@router.callback_query(FormAdmin.input_clinic)
async def main_handler(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    clinic = db.get_clinic(db_id=call.data)

    data = await state.get_data()
    admin_login = data["login"]
    admin_password = data["password"]

    admin = db.get_admin_account(name_admin=admin_login, password=admin_password, clinic_id=clinic.get_id())

    await state.clear()

    if admin is None:
        await bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            reply_markup=None
        )

        await bot.answer(
            user_id=user_id,
            text="ADMIN_INCORRECT",
            keyboard_name=KeyboardName.MAIN,
            keyboard_type=KeyboardType.REPLY,
            language_name=user_language
        )

        return False

    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    await bot.answer(
        user_id=user_id,
        text="ADMIN_SUCCESSFULL",
        keyboard_name=KeyboardName.ADMIN,
        keyboard_type=KeyboardType.REPLY,
        language_name=user_language
    )

    db.set_admin_authenticated(user_id=user_id, admin_id=admin.get_id())


@router.message(pressed_button(button_name="ADMIN_MENU_SEND_NOTIFICATIONS"))
async def main_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    admin = db.get_admin_authenticated(user_id=user_id)

    if not admin:
        return False

    await state.set_state(AdminFunc.sending_notifications)

    await bot.answer(
        user_id=user_id,
        text="ADMIN_SENDED_NOTIFICATIONS",
        language_name=user_language
    )


@router.message(AdminFunc.sending_notifications)
async def main_handler(msg: Message, state: FSMContext):

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    await state.clear()

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    photos = None
    text = None

    if msg.photo is not None:
        photos = [photo for photo in msg.photo]
        text = msg.caption
    else:
        text = msg.text

    notif_list = db.get_notifications_list()

    for us in notif_list:
        if notif_list[us]:
            try:
                if photos is not None:
                    await bot.send_photo(us, photo=photos[-1].file_id, caption=text)
                else:
                    await bot.send_message(us, text)
            except:
                continue
            # Чтобы не получить рейт лимит, каждые 1 сообщение каждые 3 секунды
            await asyncio.sleep(3)

    debug_print("Admin", user_id, "has notified all users!")

    await bot.answer(
        user_id=user_id,
        text="ADMIN_SUCCES_SEND_NOTIFICATIONS",
        keyboard_name=KeyboardName.MAIN,
        keyboard_type=KeyboardType.REPLY,
        language_name=user_language
    )

    await msg.delete()


@router.message(pressed_button(button_name="ADMIN_MENU_GET_CLINIC_INFO"))
async def main_handler(msg: Message):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    admin = db.get_admin_authenticated(user_id=user_id)

    if not admin:
        return False

    clinic = admin.get_clinic()

    appointments = db.get_appointments()

    all_appointments = len(appointments)
    success_appointments, waiting_appointments, unsuccess_appointments = 0, 0, 0

    for appointment in appointments:
        if appointment.get_status().get_name_status() == "Success":
            success_appointments += 1
        if appointment.get_status().get_name_status() == "Unsuccess":
            unsuccess_appointments += 1
        if appointment.get_status().get_name_status() == "Waiting":
            waiting_appointments += 1

    all_blood = db.get_has_blood(clinic_id=clinic.get_id())

    bloods_text = ""

    for blood in all_blood:
        bloods_text += blood.get_blood().get_blood_and_comp_name() + ": " + str(blood.get_quantity()) + " litres\n"

    message_text = message_translate(message_name="ADMIN_CLINIC_INFO", language_name=user_language) % (
        clinic.get_id(), clinic.get_clinic_name(), all_appointments, waiting_appointments, success_appointments, unsuccess_appointments, bloods_text
    )

    await bot.answer(
        user_id=user_id,
        text=message_text,
        keyboard_name=KeyboardName.MAIN,
        keyboard_type=KeyboardType.REPLY,
        language_name=user_language,
        need_translation=False
    )

@router.message(pressed_button(button_name="ADMIN_MENU_SET_STATUS"))
async def main_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    admin = db.get_admin_authenticated(user_id=user_id)

    if not admin:
        return False

    await state.set_state(AdminFunc.input_appointment_id)
 
    await bot.answer(
        user_id=user_id,
        text="ADMIN_INPUT_APPOINTMENT_ID",
        language_name=user_language
    )

    await msg.delete()
    

@router.message(AdminFunc.input_appointment_id)
async def main_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    
    admin = db.get_admin_authenticated(user_id=user_id)
    
    id_pattern = r"\d+"
    
    if not admin:
        return False
    
    if msg.text is None or not match(id_pattern, msg.text):

            bot_msg = await bot.answer(
                user_id=user_id,
                text="ADMIN_INCORRECT_APPOINTMENT_ID",
                language_name=user_language
            )

            await asyncio.sleep(5)
            await bot_msg.delete()

            return False
    
    await state.update_data(appointment_id=msg.text)
    await state.set_state(AdminFunc.input_status)
    
    await bot.answer(
        user_id=user_id,
        text="ADMIN_INPUT_STATUS",
        language_name=user_language,
        keyboard_name=KeyboardName.STATUSES,
        keyboard_type=KeyboardType.INLINE
    )

    await msg.delete()
    
@router.callback_query(AdminFunc.input_status)
async def main_handler(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    status = db.get_status(db_id=call.data)

    data = await state.get_data()
    appointment_id = data["appointment_id"]

    admin = db.get_admin_authenticated(user_id=user_id)
    
    if not admin:
        return False
    
    seccess = db.update_appointment_status(db_id=appointment_id, status_id=status.get_id())

    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    
    if seccess:
        message_text = message_translate(
            message_name="ADMIN_SUCCESSFULLY_CHANGED_STATUS",
            language_name=user_language
        ) % (appointment_id, status.get_name_status())

        await bot.answer(
            user_id=user_id,
            text=message_text,
            language_name=user_language,
            keyboard_name=KeyboardName.MAIN,
            keyboard_type=KeyboardType.REPLY,
            need_translation=False
        )
    else:
        await bot.answer(
            user_id=user_id,
            text="ADMIN_UNSUCCESSFULL_CHANGED_STATUS",
            language_name=user_language,
            keyboard_name=KeyboardName.MAIN,
            keyboard_type=KeyboardType.REPLY
        )

hnd.add_router(router)
