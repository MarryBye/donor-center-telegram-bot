import asyncio
import config as cfg

from re import match

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.classes.CRMBot import CRMBot
from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import Form
from src.classes.Datatypes.Donor import Donor
from src.classes.Datatypes.Telephone import Telephone

from src.funcs.core import language_name_to_id, gender_name_to_id

bot = CRMBot()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="Donor`s registration router")


@router.message(Command("start"))
async def main_handler(msg: Message, state: FSMContext):

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    if db.get_donor(telegram_id=user_id) is not None:

        await bot.answer(
            user_id=user_id,
            text="ALREADY_REGISTERED",
            keyboard_name=KeyboardName.MAIN,
            keyboard_type=KeyboardType.REPLY,
            language_name=user_language
        )

        return False

    db.set_user_notifications(user_id=user_id, option=True)
    db.set_user_language(user_id=user_id, language=cfg.DEFAULT_LANGUAGE, only_cache=True)

    await state.update_data(telegram_ID=user_id)
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
    user_language = db.get_language(db_id=call.data)

    db.set_user_language(user_id=user_id, language=user_language.get_lang_name(), only_cache=True)

    await state.update_data(language=user_language)
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
        language_name=user_language.get_lang_name()
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

    t = str(user_contact.phone_number)
    if not t.startswith("+"):
        t = f"+{t}"
    print(t)

    user_telephone = Telephone(data={"number": t})
    user_firstname = user_contact.first_name or "NODATA"
    user_lastname = user_contact.last_name or "NODATA"

    await state.update_data(name_donor=user_firstname)
    await state.update_data(surname_donor=user_lastname)
    await state.update_data(telephone=user_telephone)
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

    await state.update_data(date_of_birth=user_birthday)
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

    await state.update_data(gender=db.get_gender(db_id=user_gender))
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

    await state.update_data(email=user_email)
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

    await state.update_data(password=user_password)
    await state.set_state(Form.registerUser_password)

    data = await state.get_data()

    donor_form = Donor(data=data)

    db.add_donor(donor=donor_form)

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
