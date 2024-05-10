from random import choice

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import Form

from src.funcs.core import pressed_button, message_translate

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="NOTIFICATIONS ROUTER")


@router.message(pressed_button(button_name="NOTIFICATIONS_MENU_ON"))
async def main_handler(msg: Message):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    db.set_user_notifications(user_id=user_id, option=True)

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.MAIN, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="NOTIFICATIONS_ON", language_name=user_language)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


@router.message(pressed_button(button_name="NOTIFICATIONS_MENU_OFF"))
async def main_handler(msg: Message):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    db.set_user_notifications(user_id=user_id, option=False)

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.MAIN, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="NOTIFICATIONS_ON", language_name=user_language)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


hnd.add_router(router)
