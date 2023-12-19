from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from src.classes.HandlersController import HandlersController
from src.classes.KeyboardsController import KeyboardsController, KB
from config import MESSAGES_TEXT, BUTTONS_TEXT

router = Router()

rt_controller = HandlersController()
kb_controller = KeyboardsController()

MENU_BTN = BUTTONS_TEXT["MENU"]

menuOpen_msg = MESSAGES_TEXT["MENU_OPEN"]

@router.message(F.text.startswith(MENU_BTN))
async def on_command(msg: Message):
       await msg.answer(menuOpen_msg.format(MENU_BTN), 
                        reply_markup=kb_controller.get_keyboard(KB.main))
       
rt_controller.add_router(router)