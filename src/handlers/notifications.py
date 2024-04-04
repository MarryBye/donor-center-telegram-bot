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

@router.message(is_pressed_kb_button("NOTIFICATIONS_MENU_ON"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       
       db.set_user_notifications(user_id=user_id, option=True)
       
       bot_message = message_translated(user_id=user_id, key="NOTIFICATIONS_ON")
              
       await msg.reply(text=bot_message)
       
@router.message(is_pressed_kb_button("NOTIFICATIONS_MENU_OFF"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       
       db.set_user_notifications(user_id=user_id, option=False)
       
       bot_message = message_translated(user_id=user_id, key="NOTIFICATIONS_OFF")
              
       await msg.reply(text=bot_message)

hnd.add_router(router)