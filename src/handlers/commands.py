import asyncio
import config as cfg

from random import choice

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.classes.CRMBot import CRMBot
from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import Form, Feedback

from src.funcs.core import pressed_button, message_translate, button_translate

bot = CRMBot()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="COMMANDS ROUTER")

@router.message(Command("start"))
async def main_handler(msg: Message):
       
    user_id = msg.from_user.id
    
    db.set_user_notifications(user_id=user_id, option=True)
    db.set_user_language(user_id=msg.from_user.id, language=cfg.DEFAULT_LANGUAGE)
    
    new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.MAIN, keyboardType=KeyboardType.REPLY, languageName=cfg.DEFAULT_LANGUAGE)
    bot_message = message_translate(message_name="START_MESSAGE", language_name=cfg.DEFAULT_LANGUAGE)
            
    await msg.reply(text=bot_message, reply_markup=new_keyboard)
       
@router.message(Command("cancel"))
async def main_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    
    if await state.get_state() != None:
        await state.clear()

        new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.MAIN, keyboardType=KeyboardType.REPLY, languageName=user_language)
        bot_message = message_translate(message_name="CANCELLED_STATE", language_name=user_language)
                
        await msg.reply(text=bot_message, reply_markup=new_keyboard)
        
@router.message(Command("notify_all"))
async def main_handler(msg: Message, state: FSMContext):
    
    # TODO Когда в базе данных появятся админы - добавить защиту
    
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    
    photos = None
    text = None
    
    if msg.photo is not None:
        photos = [photo for photo in msg.photo]
        text = msg.caption.replace("/notify_all ", "")
    else:
        text = msg.text.replace("/notify_all ", "")

    new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.MAIN, keyboardType=KeyboardType.REPLY, languageName=user_language)
    bot_message = message_translate(message_name="CANCELLED_STATE", language_name=user_language)
    
    for user_id in enumerate(db.get_notifications_list()):
        if photos is not None:
            await bot.send_photo(user_id, photo=photos[-1].file_id, caption=text)
        else:
            await bot.send_message(user_id, text)
        # Чтобы не получить рейт лимит, каждые 1 сообщение каждые 3 секунды
        await asyncio.sleep(3)
            
    await msg.reply(text=bot_message)
       
hnd.add_router(router)