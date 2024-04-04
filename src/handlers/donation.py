from random import choice

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController
from src.classes.Form import Form

from src.funcs.core import is_pressed_kb_button, message_translated, button_translated

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router()

@router.message(is_pressed_kb_button("DONATION_MENU_REGISTER"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       
       new_keyboard = kb.get_keyboard(kb.DONATION).reload_for(user_id)
       bot_message = message_translated(user_id=user_id, key="REGISTER_STEP_1") % msg.from_user.username
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)

@router.message(is_pressed_kb_button("DONATION_MENU_FIND_CENTER"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       
       new_keyboard = kb.get_keyboard(kb.DONATION).reload_for(user_id)
       bot_message = message_translated(user_id=user_id, key="DONATION_FIND_CENTERS_MESSAGE") % (msg.from_user.username, "абоба\nабоба\nабоба")
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)
       
@router.message(is_pressed_kb_button("DONATION_MENU_HISTORY"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       
       new_keyboard = kb.get_keyboard(kb.DONATION).reload_for(user_id)
       bot_message = message_translated(user_id=user_id, key="DONATION_HISTORY_MESSAGE") % (msg.from_user.username, "7", "абоба\nабоба\nабоба")
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)

hnd.add_router(router)