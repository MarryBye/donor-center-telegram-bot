from random import choice

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import Form

from src.funcs.core import is_pressed_kb_button, message_translated

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router()

@router.message(is_pressed_kb_button("LANGUAGES_MENU_UK"))
async def language_handler(msg: Message):
    
    user_id = msg.from_user.id
    
    db.set_user_language(user_id=msg.from_user.id, language="uk-UK")
    
    user_language = db.get_user_language(user_id=user_id)
       
    new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.MAIN, keyboardType=KeyboardType.REPLY, languageName=user_language)
    bot_message = message_translated(user_id=msg.from_user.id, key="SUCCESFULLY_CHANGED_LANGUAGE")
            
    await msg.reply(text=bot_message, reply_markup=new_keyboard)
    
@router.message(is_pressed_kb_button("LANGUAGES_MENU_EN"))
async def language_handler(msg: Message):
    
    user_id = msg.from_user.id
    
    db.set_user_language(user_id=msg.from_user.id, language="en-EN")
    
    user_language = db.get_user_language(user_id=user_id)
       
    new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.MAIN, keyboardType=KeyboardType.REPLY, languageName=user_language)
    bot_message = message_translated(user_id=msg.from_user.id, key="SUCCESFULLY_CHANGED_LANGUAGE")
            
    await msg.reply(text=bot_message, reply_markup=new_keyboard)
    
@router.message(is_pressed_kb_button("LANGUAGES_MENU_RU"))
async def language_handler(msg: Message):
    
    user_id = msg.from_user.id
    
    db.set_user_language(user_id=msg.from_user.id, language="ru-RU")
    
    user_language = db.get_user_language(user_id=user_id)
       
    new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.MAIN, keyboardType=KeyboardType.REPLY, languageName=user_language)
    bot_message = message_translated(user_id=msg.from_user.id, key="SUCCESFULLY_CHANGED_LANGUAGE")
            
    await msg.reply(text=bot_message, reply_markup=new_keyboard)
    
@router.message(is_pressed_kb_button("LANGUAGES_MENU_DE"))
async def language_handler(msg: Message):
    
    user_id = msg.from_user.id
    
    db.set_user_language(user_id=msg.from_user.id, language="de-DE")
    
    user_language = db.get_user_language(user_id=user_id)
       
    new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.MAIN, keyboardType=KeyboardType.REPLY, languageName=user_language)
    bot_message = message_translated(user_id=msg.from_user.id, key="SUCCESFULLY_CHANGED_LANGUAGE")
            
    await msg.reply(text=bot_message, reply_markup=new_keyboard)
    
@router.message(is_pressed_kb_button("LANGUAGES_MENU_CN"))
async def language_handler(msg: Message):
    
    user_id = msg.from_user.id
    
    db.set_user_language(user_id=msg.from_user.id, language="cn-CN")
    
    user_language = db.get_user_language(user_id=user_id)
       
    new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.MAIN, keyboardType=KeyboardType.REPLY, languageName=user_language)
    bot_message = message_translated(user_id=msg.from_user.id, key="SUCCESFULLY_CHANGED_LANGUAGE")
            
    await msg.reply(text=bot_message, reply_markup=new_keyboard)
    
@router.message(is_pressed_kb_button("LANGUAGES_MENU_FR"))
async def language_handler(msg: Message):
    
    user_id = msg.from_user.id
    
    db.set_user_language(user_id=msg.from_user.id, language="fr-FR")
    
    user_language = db.get_user_language(user_id=user_id)
       
    new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.MAIN, keyboardType=KeyboardType.REPLY, languageName=user_language)
    bot_message = message_translated(user_id=msg.from_user.id, key="SUCCESFULLY_CHANGED_LANGUAGE")
            
    await msg.reply(text=bot_message, reply_markup=new_keyboard)

hnd.add_router(router)