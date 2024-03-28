from random import choice

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController

from src.funcs.core import is_pressed_kb_button

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router()

@router.message(Command("start"))
async def register_handler(msg: Message):
       
       new_keyboard = kb.get_keyboard(kb.REGISTRATION).reload_for(msg.from_user.id)
       await msg.reply(text="abob", reply_markup=new_keyboard)
       
@router.message(is_pressed_kb_button("REG_MENU_INFO"))
async def register_info_handler(msg: Message):
       
       db.set_user_language(user_id=msg.from_user.id, language=choice(["cn-CN", "en-EN", "ru-RU"]))
       
       new_keyboard = kb.get_keyboard(kb.REGISTRATION).reload_for(msg.from_user.id)
       await msg.reply(text="ИНФА", reply_markup=new_keyboard)
       
@router.message(is_pressed_kb_button("REG_MENU_LANGUAGES"))
async def register_info_handler(msg: Message):
       
       db.set_user_language(user_id=msg.from_user.id, language=choice(["cn-CN", "en-EN", "ru-RU"]))
       
       new_keyboard = kb.get_keyboard(kb.REGISTRATION).reload_for(msg.from_user.id)
       await msg.reply(text="ЯЗІКИ", reply_markup=new_keyboard)

hnd.add_router(router)