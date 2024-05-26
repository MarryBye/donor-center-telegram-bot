from re import match

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.classes.CRMBot import CRMBot
from src.classes.Form import UserSettings
from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType

from src.funcs.core import message_translate, gender_name_to_id


bot = CRMBot()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="PROFILE ROUTER")


@router.callback_query(lambda q: q.data == "edit_profile")
async def update_profile(call: CallbackQuery):
    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    await bot.answer_callback_query(call.id)

    new_inline_keyboard = kb.get_keyboard(
        keyboard_name=KeyboardName.PROFILE_SETTINGS,
        keyboard_type=KeyboardType.INLINE,
        language_name=user_language,
    )

    await bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=new_inline_keyboard,
    )


@router.callback_query(lambda q: q.data == "edit_name")
async def update_profile(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    await bot.answer_callback_query(call.id)

    new_text = message_translate("PROFILE_NAME_REQUEST", language_name=user_language)

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=new_text,
        reply_markup=None,
    )

    await state.set_state(UserSettings.name)


@router.message(UserSettings.name)
async def check_name(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    donor = db.get_donor(telegram_id=user_id)

    pattern = r"^[a-zA-Zа-яА-ЯёЁ]+$"
    if match(pattern, msg.text):
        db.update_donor_field(donor, "name_donor", msg.text)

        await msg.answer(
            message_translate("PROFILE_NAME_CHANGED", language_name=user_language)
        )
        await state.clear()
    else:
        await msg.answer(
            message_translate("PROFILE_NAME_ERROR", language_name=user_language)
        )


@router.callback_query(lambda q: q.data == "edit_number")
async def update_profile(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    await bot.answer_callback_query(call.id)

    new_text = message_translate("PROFILE_NUMBER_REQUEST", language_name=user_language)

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=new_text,
        reply_markup=None,
    )

    await state.set_state(UserSettings.number)


@router.message(UserSettings.number)
async def check_name(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    donor = db.get_donor(telegram_id=user_id)

    pattern = r"^\+\d{12}$"
    if match(pattern, msg.text):
        db.update_donor_field(donor, "number", msg.text)

        await msg.answer(
            message_translate("PROFILE_NUMBER_CHANGED", language_name=user_language)
        )

        await state.clear()
    else:
        await msg.answer(
            message_translate("PROFILE_NUMBER_ERROR", language_name=user_language)
        )


@router.callback_query(lambda q: q.data == "edit_bdate")
async def update_profile(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    await bot.answer_callback_query(call.id)

    new_text = message_translate("PROFILE_BDATE_REQUEST", language_name=user_language)

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=new_text,
        reply_markup=None,
    )

    await state.set_state(UserSettings.bdate)


@router.message(UserSettings.bdate)
async def check_name(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    donor = db.get_donor(telegram_id=user_id)

    birthday_pattern = (
        r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(19[4-9][0-9]|20[0-9]{2})$"
    )

    if match(birthday_pattern, msg.text):
        db.update_donor_field(donor, "date_of_birth", msg.text)

        await msg.answer(
            message_translate("PROFILE_BDATE_CHANGED", language_name=user_language)
        )

        await state.clear()
    else:
        await msg.answer(
            message_translate("PROFILE_BDATE_ERROR", language_name=user_language)
        )


@router.callback_query(lambda q: q.data == "edit_gender")
async def update_profile(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    await bot.answer_callback_query(call.id)

    new_text = message_translate("PROFILE_GENDER_REQUEST", language_name=user_language)
    new_keyboard = kb.get_keyboard(
        keyboard_name=KeyboardName.GENDERS,
        keyboard_type=KeyboardType.INLINE,
        language_name=user_language,
    )

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=new_text,
        reply_markup=new_keyboard,
    )

    await state.set_state(UserSettings.gender)


@router.callback_query(UserSettings.gender)
async def check_name(call: Message, state: FSMContext):
    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    donor = db.get_donor(telegram_id=user_id)

    gender_id = call.data

    db.update_donor_field(donor, "gender_ID", gender_id)

    await bot.answer_callback_query(call.id)
    new_text = message_translate("PROFILE_GENDER_CHANGED", language_name=user_language)

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=new_text,
        reply_markup=None,
    )

    await state.clear()


@router.callback_query(lambda q: q.data == "edit_email")
async def update_profile(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    await bot.answer_callback_query(call.id)

    new_text = message_translate("PROFILE_EMAIL_REQUEST", language_name=user_language)

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=new_text,
        reply_markup=None,
    )

    await state.set_state(UserSettings.email)


@router.message(UserSettings.email)
async def check_name(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    donor = db.get_donor(telegram_id=user_id)

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if match(pattern, msg.text):
        db.update_donor_field(donor, "email", msg.text)

        await msg.answer(
            message_translate("PROFILE_EMAIL_CHANGED", language_name=user_language)
        )
        await state.clear()
    else:
        await msg.answer(
            message_translate("PROFILE_EMAIL_ERROR", language_name=user_language)
        )


hnd.add_router(router)
