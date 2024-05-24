import asyncio
import config as cfg

from re import match

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.classes.CRMBot import CRMBot
from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.Controllers.DonorsDatabaseController import DonorsDatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import Form
from src.classes.Datatypes.Donor import Donor

from src.funcs.core import language_name_to_id, gender_name_to_id

bot = CRMBot()

db = DatabaseController()
donors_db = DonorsDatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="Donor`s registration router")


@router.message(Command("start"))
async def main_handler(msg: Message, state: FSMContext):

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    if not donors_db.get_donor_by(telegram_id=user_id).is_empty():

        await bot.answer(
            user_id=user_id,
            text="ALREADY_REGISTERED",
            keyboard_name=KeyboardName.MAIN,
            keyboard_type=KeyboardType.REPLY,
            language_name=user_language
        )

        return False

    donor_data = Donor()
    donor_data.set_telegram(telegram_id=user_id)

    db.set_user_notifications(user_id=user_id, option=True)
    db.set_user_language(user_id=user_id, language=cfg.DEFAULT_LANGUAGE, only_cache=True)

    await state.update_data(donor_data=donor_data)
    await state.set_state(Form.registerUser_language)

    await bot.answer(
        user_id=user_id,
        text="REGISTER_START",
        keyboard_name=KeyboardName.LANGUAGES_REGISTER,
        keyboard_type=KeyboardType.INLINE,
        language_name=user_language
    )


@router.callback_query(Form.registerUser_language)
async def main_handler(call: CallbackQuery, state: FSMContext):

    user_id = call.from_user.id
    user_language = call.data

    donor_data = await state.get_data()
    donor_data["donor_data"].set_language(language_id=language_name_to_id(user_language))

    db.set_user_language(user_id=user_id, language=user_language, only_cache=True)

    await state.update_data(donor_data=donor_data["donor_data"])
    await state.set_state(Form.registerUser_contact)

    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    await bot.answer(
        user_id=user_id,
        text="REGISTER_STEP_1",
        keyboard_name=KeyboardName.MSG_SHARECONTACT,
        keyboard_type=KeyboardType.REPLY,
        language_name=user_language
    )


@router.message(Form.registerUser_contact)
async def main_handler(msg: Message, state: FSMContext):

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    user_contact = msg.contact

    if user_contact is None:

        bot_msg = await bot.answer(
            user_id=user_id,
            text="REGISTER_STEP_1_FAILURE",
            keyboard_name=KeyboardName.MSG_SHARECONTACT,
            keyboard_type=KeyboardType.REPLY,
            language_name=user_language
        )

        await asyncio.sleep(5)
        await bot_msg.delete()

        return False

    user_phone = user_contact.phone_number
    user_firstname = user_contact.first_name or "NODATA"
    user_lastname = user_contact.last_name or "NODATA"

    donor_data = await state.get_data()
    donor_data["donor_data"].set_name(name=user_firstname)
    donor_data["donor_data"].set_surname(surname=user_lastname)
    donor_data["donor_data"].set_number(number=user_phone)

    await state.update_data(donor_data=donor_data["donor_data"])
    await state.set_state(Form.registerUser_birthday)

    await bot.answer(
        user_id=user_id,
        text="REGISTER_STEP_2",
        language_name=user_language
    )

    await msg.delete()


@router.message(Form.registerUser_birthday)
async def main_handler(msg: Message, state: FSMContext):

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    user_birthday = msg.text

    birthday_pattern = r'^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(19[4-9][0-9]|20[0-9]{2})$'

    if msg.text is None or not match(birthday_pattern, msg.text):

        bot_msg = await bot.answer(
            user_id=user_id,
            text="REGISTER_STEP_2_FAILURE",
            language_name=user_language
        )

        await asyncio.sleep(5)
        await bot_msg.delete()

        return False

    donor_data = await state.get_data()
    donor_data["donor_data"].set_birthdate(birthdate=user_birthday)

    await state.update_data(donor_data=donor_data["donor_data"])
    await state.set_state(Form.registerUser_gender)

    await bot.answer(
        user_id=user_id,
        text="REGISTER_STEP_3",
        keyboard_name=KeyboardName.GENDERS,
        keyboard_type=KeyboardType.INLINE,
        language_name=user_language
    )

    await msg.delete()


@router.callback_query(Form.registerUser_gender)
async def main_handler(call: CallbackQuery, state: FSMContext):

    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    user_gender = call.data

    donor_data = await state.get_data()
    donor_data["donor_data"].set_gender(gender_id=gender_name_to_id(user_gender))

    await state.update_data(donor_data=donor_data["donor_data"])
    await state.set_state(Form.registerUser_email)

    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    await bot.answer(
        user_id=user_id,
        text="REGISTER_STEP_4",
        language_name=user_language
    )


@router.message(Form.registerUser_email)
async def main_handler(msg: Message, state: FSMContext):

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    user_email = msg.text

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if msg.text is None or not match(email_pattern, msg.text):

        bot_msg = await bot.answer(
            user_id=user_id,
            text="REGISTER_STEP_4_FAILURE",
            language_name=user_language
        )

        await asyncio.sleep(5)
        await bot_msg.delete()

        return False

    donor_data = await state.get_data()
    donor_data["donor_data"].set_email(email=user_email)

    await state.update_data(donor_data=donor_data["donor_data"])
    await state.set_state(Form.registerUser_password)

    await bot.answer(
        user_id=user_id,
        text="REGISTER_STEP_5",
        language_name=user_language
    )

    await msg.delete()


@router.message(Form.registerUser_password)
async def main_handler(msg: Message, state: FSMContext):

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    user_password = msg.text

    password_pattern = r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z0-9]{8,}$'

    if msg.text is None or not match(password_pattern, msg.text):

        bot_msg = await bot.answer(
            user_id=user_id,
            text="REGISTER_STEP_5_FAILURE",
            language_name=user_language
        )

        await asyncio.sleep(5)
        await bot_msg.delete()

        return False

    donor_data = await state.get_data()
    donor_data["donor_data"].set_password(password=user_password)

    donors_db.register_donor(donor=donor_data["donor_data"])

    await state.clear()

    await bot.answer(
        user_id=user_id,
        text="SUCCESSFULL_REGISTER",
        keyboard_name=KeyboardName.MAIN,
        keyboard_type=KeyboardType.REPLY,
        language_name=user_language
    )

    await msg.delete()


hnd.add_router(router)
