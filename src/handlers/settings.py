from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from src.classes.HandlersController import HandlersController
from src.classes.KeyboardsController import KeyboardsController, KB
from config import MESSAGES_TEXT, BUTTONS_TEXT

router = Router()

rt_controller = HandlersController()
kb_controller = KeyboardsController()

MENU_BUTTONS = BUTTONS_TEXT["SETTINGS_MENU"]
NOTIFICATIONS_BTN = MENU_BUTTONS["NOTIFICATIONS"]
SECURITY_BTN = MENU_BUTTONS["SECURITY"]

menuOpen_msg = MESSAGES_TEXT["MENU_OPEN"]

@router.message(F.text.startswith(NOTIFICATIONS_BTN))
async def get_register(msg: Message):
       await msg.answer(menuOpen_msg.format(NOTIFICATIONS_BTN))

@router.message(F.text.startswith(SECURITY_BTN))
async def get_info(msg: Message):
       await msg.answer(menuOpen_msg.format(SECURITY_BTN))
       
rt_controller.add_router(router)