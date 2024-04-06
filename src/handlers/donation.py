from random import choice

from aiogram import Router
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.classes.CRMBot import CRMBot
from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import Form

from src.funcs.core import is_pressed_kb_button, is_sended_callback, message_translated

bot = CRMBot()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router()

@router.message(is_pressed_kb_button("DONATION_MENU_REGISTER"))
async def main_handler(msg: Message, state: FSMContext):
       
       user_id = msg.from_user.id
       user_language = db.get_user_language(user_id=user_id)
       
       if not db.get_donor(user_id=user_id):
              await state.set_state(Form.sendContact)
              
              new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.MSG_SHARECONTACT, keyboardType=KeyboardType.REPLY, languageName=user_language)
              bot_message = message_translated(user_id=user_id, key="REGISTER_STEP_1") % msg.from_user.username
              
              await msg.reply(text=bot_message, reply_markup=new_keyboard)
       else:
              new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.DONATION, keyboardType=KeyboardType.REPLY, languageName=user_language)
              bot_message = message_translated(user_id=user_id, key="CANNOT_REGISTER")
                     
              await msg.reply(text=bot_message, reply_markup=new_keyboard)
              
@router.callback_query(is_sended_callback("send_contact"), Form.sendContact)
async def main_handler(callback: CallbackQuery, state: FSMContext):
       await state.clear()
       
       user = callback.from_user
       contact = callback.from_user.contact
       print(user.phone_number)
       
       await bot.edit_message_reply_markup(
              chat_id=callback.from_user.id,
              message_id=callback.message.message_id, 
              reply_markup=None
       )
       
@router.message(is_pressed_kb_button("DONATION_MENU_FIND_CENTER"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       user_language = db.get_user_language(user_id=user_id)
       
       new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.DONATION, keyboardType=KeyboardType.REPLY, languageName=user_language)
       bot_message = message_translated(user_id=user_id, key="DONATION_FIND_CENTERS_MESSAGE") % (msg.from_user.username, "абоба\nабоба\nабоба")
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)
       
@router.message(is_pressed_kb_button("DONATION_MENU_HISTORY"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       user_language = db.get_user_language(user_id=user_id)
       
       new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.DONATION, keyboardType=KeyboardType.REPLY, languageName=user_language)
       bot_message = message_translated(user_id=user_id, key="DONATION_HISTORY_MESSAGE") % (msg.from_user.username, "7", "абоба\nабоба\nабоба")
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)

hnd.add_router(router)