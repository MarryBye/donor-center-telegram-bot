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
       
@router.message(is_pressed_kb_button("BUTTON_HOME"))
async def main_handler(msg: Message):
       await state.clear()
       
       user_id = msg.from_user.id
       
       new_keyboard = kb.get_keyboard(kb.MAIN).reload_for(user_id)
       bot_message = message_translated(user_id=user_id, key="MENU_OPEN") % button_translated(user_id=user_id, key="BUTTON_HOME")
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)

hnd.add_router(router)
