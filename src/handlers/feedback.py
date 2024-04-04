from re import match
import string
from aiocache import Cache

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.classes.Form import Feedback
from src.classes.Keyboards import KeyboardController
from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController

from src.funcs.core import is_pressed_kb_button, message_translated, button_translated

cache = Cache()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router()


@router.message(Feedback.name)
async def process_name(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    name = msg.text.strip()
    new_keyboard = kb.get_keyboard(kb.FEEDBACK).reload_for(user_id)
    bot_message = message_translated(user_id, key="FEEDBACK_AFTER_NAME_MESSAGE")

    if not name.isdigit():
        await state.update_data(name=name)
        await cache.set(f"user:{user_id}:name", name)
        await state.clear()
        await msg.answer(bot_message, reply_markup=new_keyboard)
    else:
        await msg.answer(message_translated(user_id, key="MAIL_PHONE_ERROR"))


@router.message(is_pressed_kb_button("FEEDBACK_MENU_PHONE"))
async def feedback_phone_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id

    new_keyboard = kb.get_keyboard(kb.MENUBACK).reload_for(user_id)
    bot_message = message_translated(user_id, key="FEEDBACK_PHONE_MESSAGE")

    await state.set_state(Feedback.phone)
    await msg.answer(bot_message, reply_markup=new_keyboard)


@router.message(Feedback.phone)
async def process_phone(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    phone = msg.text
    allowed_chars = set(string.ascii_letters)

    new_keyboard = kb.get_keyboard(kb.MENUBACK).reload_for(user_id)
    bot_message = message_translated(user_id, key="PHONE_SENT")

    if match(r"^(\+?\d{1,4}[\s-])?(?!0+\d)\d{10,15}$", phone):
        await msg.answer(bot_message, reply_markup=new_keyboard)
        await state.clear()

        name = await cache.get(f"user:{user_id}:name")

        print(phone, name)

        # TODO: phone sending...
    else:
        await msg.answer(message_translated(user_id, key="MAIL_PHONE_ERROR"))
        print("phone error")


@router.message(is_pressed_kb_button("FEEDBACK_MENU_MAIL"))
async def feedback_mail_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id

    new_keyboard = kb.get_keyboard(kb.MENUBACK).reload_for(user_id)
    bot_message = message_translated(user_id, key="FEEDBACK_MAIL_MESSAGE")

    await state.set_state(Feedback.mail)
    await msg.answer(bot_message, reply_markup=new_keyboard)


@router.message(Feedback.mail)
async def process_phone(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    mail = msg.text

    new_keyboard = kb.get_keyboard(kb.MENUBACK).reload_for(user_id)
    bot_message = message_translated(user_id, key="MAIL_SENT")

    if match(r"^[^@]+@[^@]+\.[^@]+$", mail):
        await msg.answer(bot_message, reply_markup=new_keyboard)
        await state.clear()

        name = await cache.get(f"user:{user_id}:name")

        print(mail, name)

        # TODO: mail sending...
    else:
        await msg.answer(message_translated(user_id, key="MAIL_PHONE_ERROR"))
        print("mail error")


hnd.add_router(router)
