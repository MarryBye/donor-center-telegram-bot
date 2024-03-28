from random import choice

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController
from src.classes.Form import RegisterForm

from src.funcs.core import is_pressed_kb_button, message_translated

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router()

@router.message(is_pressed_kb_button("LANGUAGES_MENU_UK"))
async def language_handler(msg: Message):
    
    db.set_user_language(user_id=msg.from_user.id, language="uk-UK")
       
    new_keyboard = kb.get_keyboard(kb.MAIN).reload_for(msg.from_user.id)
    bot_message = message_translated(user_id=msg.from_user.id, key="SUCCESFULLY_CHANGED_LANGUAGE")
            
    await msg.reply(text=bot_message, reply_markup=new_keyboard)
    
@router.message(is_pressed_kb_button("LANGUAGES_MENU_EN"))
async def language_handler(msg: Message):
    
    db.set_user_language(user_id=msg.from_user.id, language="en-EN")
       
    new_keyboard = kb.get_keyboard(kb.MAIN).reload_for(msg.from_user.id)
    bot_message = message_translated(user_id=msg.from_user.id, key="SUCCESFULLY_CHANGED_LANGUAGE")
            
    await msg.reply(text=bot_message, reply_markup=new_keyboard)
    
@router.message(is_pressed_kb_button("LANGUAGES_MENU_RU"))
async def language_handler(msg: Message):
    
    db.set_user_language(user_id=msg.from_user.id, language="ru-RU")
       
    new_keyboard = kb.get_keyboard(kb.MAIN).reload_for(msg.from_user.id)
    bot_message = message_translated(user_id=msg.from_user.id, key="SUCCESFULLY_CHANGED_LANGUAGE")
            
    await msg.reply(text=bot_message, reply_markup=new_keyboard)
    
@router.message(is_pressed_kb_button("LANGUAGES_MENU_DE"))
async def language_handler(msg: Message):
    
    db.set_user_language(user_id=msg.from_user.id, language="de-DE")
       
    new_keyboard = kb.get_keyboard(kb.MAIN).reload_for(msg.from_user.id)
    bot_message = message_translated(user_id=msg.from_user.id, key="SUCCESFULLY_CHANGED_LANGUAGE")
            
    await msg.reply(text=bot_message, reply_markup=new_keyboard)
    
@router.message(is_pressed_kb_button("LANGUAGES_MENU_CN"))
async def language_handler(msg: Message):
    
    db.set_user_language(user_id=msg.from_user.id, language="cn-CN")
       
    new_keyboard = kb.get_keyboard(kb.MAIN).reload_for(msg.from_user.id)
    bot_message = message_translated(user_id=msg.from_user.id, key="SUCCESFULLY_CHANGED_LANGUAGE")
            
    await msg.reply(text=bot_message, reply_markup=new_keyboard)
    
@router.message(is_pressed_kb_button("LANGUAGES_MENU_FR"))
async def language_handler(msg: Message):
    
    db.set_user_language(user_id=msg.from_user.id, language="fr-FR")
       
    new_keyboard = kb.get_keyboard(kb.MAIN).reload_for(msg.from_user.id)
    bot_message = message_translated(user_id=msg.from_user.id, key="SUCCESFULLY_CHANGED_LANGUAGE")
            
    await msg.reply(text=bot_message, reply_markup=new_keyboard)

hnd.add_router(router)