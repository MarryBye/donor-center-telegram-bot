import config as cfg

from random import choice

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import Form, Feedback

from src.funcs.core import pressed_button, message_translate, button_translate

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router()

@router.message(Command("start"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       
       db.set_user_notifications(user_id=user_id, option=True)
       db.set_user_language(user_id=msg.from_user.id, language=cfg.DEFAULT_LANGUAGE)
       
       new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.MAIN, keyboardType=KeyboardType.REPLY, languageName=cfg.DEFAULT_LANGUAGE)
       bot_message = message_translate(message_name="START_MESSAGE", language_name=cfg.DEFAULT_LANGUAGE)
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)

@router.message(pressed_button(button_name="MAIN_MENU_DONATION"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       user_language = db.get_user_language(user_id=user_id)
       
       new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.DONATION, keyboardType=KeyboardType.REPLY, languageName=user_language)
       bot_message = message_translate(message_name="MENU_OPEN", language_name=user_language) % button_translate(button_name="MAIN_MENU_DONATION", language_name=user_language)
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)

@router.message(pressed_button(button_name="MAIN_MENU_INFO"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       user_language = db.get_user_language(user_id=user_id)
       
       bot_message = message_translate(message_name="INFO_REGISTER", language_name=user_language)
              
       await msg.reply(text=bot_message)
       
@router.message(pressed_button(button_name="MAIN_MENU_SETTINGS"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       user_language = db.get_user_language(user_id=user_id)
       
       new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.SETTINGS, keyboardType=KeyboardType.REPLY, languageName=user_language)
       bot_message = message_translate(message_name="MENU_OPEN", language_name=user_language) % button_translate(button_name="MAIN_MENU_DONATION", language_name=user_language)
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)
       
@router.message(pressed_button(button_name="MAIN_MENU_FEEDBACK"))
async def feedback_handler(msg: Message, state: FSMContext):

       user_id = msg.from_user.id
       user_language = db.get_user_language(user_id=user_id)

       new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.FEEDBACK, keyboardType=KeyboardType.REPLY, languageName=user_language)
       bot_message = message_translate(message_name="FEEDBACK_MENU_OPEN", language_name=user_language) % button_translate(button_name="MAIN_MENU_FEEDBACK", language_name=user_language)
       
       await msg.reply(bot_message, reply_markup=new_keyboard)

       # TODO: если имя есть в бд, то пропустить шаг с ним
       # if not name_in_db:

       await state.set_state(Feedback.name)
       
       new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.MENUBACK, keyboardType=KeyboardType.REPLY, languageName=user_language)
       bot_message = message_translate(message_name="NAME_SENT", language_name=user_language)
       
       await msg.answer(bot_message, reply_markup=new_keyboard)

hnd.add_router(router)
