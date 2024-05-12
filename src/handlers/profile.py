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
from src.classes.Form import Form, Feedback, UserSettings
from src.classes.Donor import Donor

from src.funcs.core import (
    pressed_button,
    message_translate,
    button_translate,
    language_name_to_id,
    gender_name_to_id,
    get_command_variations,
    sent_callback,
)

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
async def check_name(msg: Message):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    # TODO: check condition

    await msg.answer(
        message_translate("PROFILE_NAME_CHANGED", language_name=user_language)
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
async def check_name(msg: Message):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    # TODO: check condition

    await msg.answer(
        message_translate("PROFILE_NUMBER_CHANGED", language_name=user_language)
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
async def check_name(msg: Message):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    # TODO: check condition

    await msg.answer(
        message_translate("PROFILE_BDATE_CHANGED", language_name=user_language)
    )


@router.callback_query(lambda q: q.data == "edit_gender")
async def update_profile(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    await bot.answer_callback_query(call.id)

    new_text = message_translate("PROFILE_GENDER_REQUEST", language_name=user_language)

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=new_text,
        reply_markup=None,
    )

    await state.set_state(UserSettings.gender)


@router.message(UserSettings.gender)
async def check_name(msg: Message):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    # TODO: check condition

    await msg.answer(
        message_translate("PROFILE_GENDER_CHANGED", language_name=user_language)
    )


hnd.add_router(router)
