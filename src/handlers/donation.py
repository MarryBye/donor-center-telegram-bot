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

from src.funcs.core import pressed_button, message_translate, language_name_to_number

bot = CRMBot()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router()

@router.message(pressed_button(button_name="DONATION_MENU_REGISTER"))
async def main_handler(msg: Message, state: FSMContext):
       
       user_id = msg.from_user.id
       user_language = db.get_user_language(user_id=user_id)
       
       if not db.get_donor(user_id=user_id):
              await state.set_state(Form.sendContact)
              
              new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.MSG_SHARECONTACT, keyboardType=KeyboardType.REPLY, languageName=user_language)
              bot_message = message_translate(message_name="REGISTER_STEP_1", language_name=user_language) % msg.from_user.username
              
              await msg.reply(text=bot_message, reply_markup=new_keyboard)
       else:
              new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.DONATION, keyboardType=KeyboardType.REPLY, languageName=user_language)
              bot_message = message_translate(message_name="CANNOT_REGISTER", language_name=user_language)
                     
              await msg.reply(text=bot_message, reply_markup=new_keyboard)
              
@router.message(Form.sendContact)
@router.message(pressed_button(button_name="SEND_CONTACT"))
async def main_handler(msg: Message, state: FSMContext):
       await state.clear()
       
       user_id = msg.from_user.id
       user_language = db.get_user_language(user_id=user_id)
       user_contact = msg.contact
       
       new_phone_id = db.get_last_id_phone() + 1  
       
       db.register_donor(id=user_id, name=user_contact.first_name, firstname=user_contact.last_name, language=language_name_to_number(user_language), phone=user_contact.phone_number)
       
@router.message(pressed_button(button_name="DONATION_MENU_FIND_CENTER"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       user_language = db.get_user_language(user_id=user_id)
       
       new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.DONATION, keyboardType=KeyboardType.REPLY, languageName=user_language)
       bot_message = message_translate(message_name="DONATION_FIND_CENTERS_MESSAGE", language_name=user_language) % (msg.from_user.username, "абоба\nабоба\nабоба")
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)
       
@router.message(pressed_button(button_name="DONATION_MENU_HISTORY"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       user_language = db.get_user_language(user_id=user_id)
       
       new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.DONATION, keyboardType=KeyboardType.REPLY, languageName=user_language)
       bot_message = message_translate(message_name="DONATION_HISTORY_MESSAGE", language_name=user_language) % (msg.from_user.username, "7", "абоба\nабоба\nабоба")
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)

hnd.add_router(router)