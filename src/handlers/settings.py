from random import choice

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import Form

from src.funcs.core import is_pressed_kb_button, message_translated, button_translated

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router()

@router.message(is_pressed_kb_button("SETTINGS_MENU_NOTIFICATIONS"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       user_language = db.get_user_language(user_id=user_id)
       
       new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.NOTIFICATIONS, keyboardType=KeyboardType.REPLY, languageName=user_language)
       bot_message = message_translated(user_id=user_id, key="MENU_OPEN") % button_translated(user_id=user_id, key="SETTINGS_MENU_NOTIFICATIONS")
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)
       
@router.message(is_pressed_kb_button("SETTINGS_MENU_LANGUAGES"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       user_language = db.get_user_language(user_id=user_id)
       
       new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.LANGUAGES, keyboardType=KeyboardType.REPLY, languageName=user_language)
       bot_message = message_translated(user_id=user_id, key="MENU_OPEN") % button_translated(user_id=user_id, key="SETTINGS_MENU_LANGUAGES")
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)

hnd.add_router(router)