from random import choice

from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController

from src.funcs.core import get_multilang_button

router = Router()

@router.message(Command("start"))
async def register_handler(msg: Message):
       
       new_keyboard = KeyboardController().get_keyboard(KeyboardController().REGISTRATION).reload_for(msg.from_user.id)
       await msg.reply(text="abob", reply_markup=new_keyboard)
       
@router.message(F.text.in_(get_multilang_button("REG_MENU_INFO")))
async def register_info_handler(msg: Message):
       
       DatabaseController().set_user_language(user_id=msg.from_user.id, language=choice(["cn-CN", "en-EN", "ru-RU"]))
       
       new_keyboard = KeyboardController().get_keyboard(KeyboardController().REGISTRATION).reload_for(msg.from_user.id)
       await msg.reply(text="abob", reply_markup=new_keyboard)

HandlersController().add_router(router)