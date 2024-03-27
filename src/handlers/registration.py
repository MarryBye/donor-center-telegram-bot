from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController

from src.funcs.core import get_language_phrases, is_authorized

router = Router()

@router.message(Command("start"))
async def register_handler(msg: Message):
       await msg.reply(text="abob", reply_markup=KeyboardController().get_keyboard(KeyboardController().REGISTRATION))
       
@router.message(F.text.startswith())

HandlersController().add_router(router)