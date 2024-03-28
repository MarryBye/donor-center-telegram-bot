from random import choice

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController
from src.classes.Form import RegisterForm

from src.funcs.core import is_pressed_kb_button, message_translated, button_translated

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router()

@router.message(is_pressed_kb_button("SETTINGS_MENU_NOTIFICATIONS"))
async def main_handler(msg: Message):
       
    user_id = msg.from_user.id
    return
       
@router.message(is_pressed_kb_button("SETTINGS_MENU_SECURITY"))
async def main_handler(msg: Message):
       
    user_id = msg.from_user.id
    return
       
@router.message(is_pressed_kb_button("SETTINGS_MENU_LANGUAGES"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       
       new_keyboard = kb.get_keyboard(kb.LANGUAGES).reload_for(user_id)
       bot_message = message_translated(user_id=user_id, key="MENU_OPEN") % button_translated(user_id=user_id, key="SETTINGS_MENU_LANGUAGES")
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)

hnd.add_router(router)