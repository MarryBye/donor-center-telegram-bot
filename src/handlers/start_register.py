import asyncio
import config as cfg

from re import match
from random import choice

from aiogram import Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.classes.CRMBot import CRMBot
from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import Form, Feedback
from src.classes.Donor import Donor

from src.funcs.core import pressed_button, message_translate, button_translate, language_name_to_id, gender_name_to_id, \
    get_command_variations, sent_callback

bot = CRMBot()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="REGISTER ROUTER")


@router.message(Command("start"))
async def main_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id

    if db.get_donor_by(telegram_id=user_id).is_empty():

        await state.set_state(Form.registerUser_language)

        donor_data = Donor()
        donor_data.set_telegram(telegram_id=user_id)

        await state.update_data(donor_data=donor_data)

        db.set_user_notifications(user_id=user_id, option=True)
        db.set_user_language(donor=donor_data, language=cfg.DEFAULT_LANGUAGE, only_cache=True)

        new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.LANGUAGES_REGISTER, keyboard_type=KeyboardType.INLINE,
                                       language_name=cfg.DEFAULT_LANGUAGE)
        bot_message = message_translate(message_name="REGISTER_START", language_name=cfg.DEFAULT_LANGUAGE)

        await msg.reply(text=bot_message, reply_markup=new_keyboard)

    else:

        new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.MAIN, keyboard_type=KeyboardType.REPLY,
                                       language_name=cfg.DEFAULT_LANGUAGE)
        bot_message = message_translate(message_name="ALREADY_REGISTERED", language_name=cfg.DEFAULT_LANGUAGE)

        bot_msg = await bot.send_message(user_id, text=bot_message, reply_markup=new_keyboard)

        await asyncio.sleep(5)
        await bot_msg.delete()


@router.callback_query(Form.registerUser_language)
async def main_handler(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_language = call.data

    donor_data = await state.get_data()
    donor_data["donor_data"].set_language(language_id=language_name_to_id(user_language))

    db.set_user_language(donor=donor_data["donor_data"], language=user_language, only_cache=True)

    await state.update_data(donor_data=donor_data["donor_data"])
    await state.set_state(Form.registerUser_contact)

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.MSG_SHARECONTACT, keyboard_type=KeyboardType.REPLY,
                                   language_name=cfg.DEFAULT_LANGUAGE)
    bot_message = message_translate(message_name="REGISTER_START", language_name=user_language)

    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    await bot.send_message(user_id, text=bot_message, reply_markup=new_keyboard)


@router.message(Form.registerUser_contact)
async def main_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    user_contact = msg.contact

    if user_contact is not None:

        user_phone = user_contact.phone_number
        user_firstname = user_contact.first_name or "NODATA"
        user_lastname = user_contact.last_name or "NODATA"

        donor_data = await state.get_data()
        donor_data["donor_data"].set_name(name=user_firstname)
        donor_data["donor_data"].set_surname(surname=user_lastname)
        donor_data["donor_data"].set_number(number=user_phone)

        await state.update_data(donor_data=donor_data["donor_data"])
        await state.set_state(Form.registerUser_birthday)

        bot_message = message_translate(message_name="REGISTER_STEP_1", language_name=user_language)

        await bot.send_message(user_id, text=bot_message, reply_markup=ReplyKeyboardRemove())

    else:
        new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.MSG_SHARECONTACT, keyboard_type=KeyboardType.REPLY,
                                       language_name=cfg.DEFAULT_LANGUAGE)
        bot_message = message_translate(message_name="REGISTER_START_FAILURE", language_name=user_language)

        bot_msg = await bot.send_message(user_id, text=bot_message, reply_markup=new_keyboard)

        await asyncio.sleep(5)
        await bot_msg.delete()

    await msg.delete()


@router.message(Form.registerUser_birthday)
async def main_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    birthday_pattern = r'^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(19[4-9][0-9]|20[0-9]{2})$'

    if msg.text is None or not match(birthday_pattern, msg.text):
        bot_message = message_translate(message_name="REGISTER_STEP_1_FAILURE", language_name=user_language)

        bot_msg = await bot.send_message(user_id, text=bot_message, reply_markup=None)

        await asyncio.sleep(5)
        await bot_msg.delete()

    elif match(birthday_pattern, msg.text):
        user_birthday = msg.text

        donor_data = await state.get_data()
        donor_data["donor_data"].set_birthdate(birthdate=user_birthday)

        await state.update_data(donor_data=donor_data["donor_data"])
        await state.set_state(Form.registerUser_gender)

        new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.GENDERS, keyboard_type=KeyboardType.INLINE,
                                       language_name=user_language)
        bot_message = message_translate(message_name="REGISTER_STEP_2", language_name=user_language)

        await bot.send_message(user_id, text=bot_message, reply_markup=new_keyboard)

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

    bot_message = message_translate(message_name="REGISTER_STEP_3", language_name=user_language)

    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    await bot.send_message(user_id, text=bot_message, reply_markup=None)

@router.message(Form.registerUser_email)
async def main_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if msg.text is None or not match(email_pattern, msg.text):
        bot_message = message_translate(message_name="REGISTER_STEP_3_FAILURE", language_name=user_language)

        bot_msg = await bot.send_message(user_id, text=bot_message, reply_markup=None)

        await asyncio.sleep(5)
        await bot_msg.delete()

    elif match(email_pattern, msg.text):

        user_email = msg.text

        donor_data = await state.get_data()
        donor_data["donor_data"].set_email(email=user_email)

        await state.update_data(donor_data=donor_data["donor_data"])
        await state.set_state(Form.registerUser_password)

        bot_message = message_translate(message_name="REGISTER_STEP_3", language_name=user_language)

        await bot.send_message(user_id, text=bot_message, reply_markup=None)

    await msg.delete()


@router.message(Form.registerUser_password)
async def main_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    password_pattern = r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z0-9]{8,}$'

    if msg.text is None or not match(password_pattern, msg.text):
        bot_message = message_translate(message_name="REGISTER_STEP_3_FAILURE", language_name=user_language)

        await bot.send_message(user_id, text=bot_message, reply_markup=None)

    elif match(password_pattern, msg.text):
        user_password = msg.text

        donor_data = await state.get_data()
        donor_data["donor_data"].set_password(password=user_password)

        db.register_donor(donor=donor_data["donor_data"])

        new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.MAIN, keyboard_type=KeyboardType.REPLY,
                                       language_name=cfg.DEFAULT_LANGUAGE)
        bot_message = message_translate(message_name="SUCCESSFULL_REGISTER", language_name=user_language)

        await state.clear()

        await bot.send_message(user_id, text=bot_message, reply_markup=new_keyboard)

    await msg.delete()


hnd.add_router(router)
