from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from src.classes.HandlersController import HandlersController
from src.classes.KeyboardsController import KeyboardsController, KB
from src.classes.DatabaseController import DatabaseController
from config import MESSAGES_TEXT, BUTTONS_TEXT

router = Router()

rt_controller = HandlersController()
kb_controller = KeyboardsController()

MENU_BUTTONS = BUTTONS_TEXT["MAIN_MENU"]
DONATION_BTN = MENU_BUTTONS["DONATION"]
SETTINGS_BTN = MENU_BUTTONS["SETTINGS"]
FEEDBACK_BTN = MENU_BUTTONS["FEEDBACK"]
LANGUAGES_BTN = MENU_BUTTONS["LANGUAGES"]

menuOpen_msg = MESSAGES_TEXT["MENU_OPEN"]

@router.message(F.text.startswith(DONATION_BTN))
async def on_command(msg: Message):
       if not DatabaseController().get_user(id=msg.from_user.id):
              return
       
       await msg.answer(menuOpen_msg.format(DONATION_BTN), 
                     reply_markup=kb_controller.get_keyboard(KB.donation))

@router.message(F.text.startswith(SETTINGS_BTN))
async def on_command(msg: Message):
       if not DatabaseController().get_user(id=msg.from_user.id):
              return
       
       await msg.answer(menuOpen_msg.format(SETTINGS_BTN), 
                        reply_markup=kb_controller.get_keyboard(KB.settings))

@router.message(F.text.startswith(FEEDBACK_BTN))
async def on_command(msg: Message):
       if not DatabaseController().get_user(id=msg.from_user.id):
              return
       
       await msg.answer(menuOpen_msg.format(FEEDBACK_BTN), 
                        reply_markup=kb_controller.get_keyboard(KB.feedback))

@router.message(F.text.startswith(LANGUAGES_BTN))
async def on_command(msg: Message):
       if not DatabaseController().get_user(id=msg.from_user.id):
              return
       
       await msg.answer(menuOpen_msg.format(LANGUAGES_BTN), 
                        reply_markup=kb_controller.get_keyboard(KB.languages))
       
rt_controller.add_router(router)