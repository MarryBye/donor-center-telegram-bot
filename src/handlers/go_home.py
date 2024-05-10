from random import choice

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import Form

from src.funcs.core import pressed_button, message_translate, button_translate

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="GO_HOME ROUTER")


@router.message(pressed_button(button_name="BUTTON_HOME"))
async def main_handler(msg: Message, state: FSMContext):
    await state.clear()

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.MAIN, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="MENU_OPEN", language_name=user_language) % button_translate(
        button_name="BUTTON_HOME", language_name=user_language)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


hnd.add_router(router)
