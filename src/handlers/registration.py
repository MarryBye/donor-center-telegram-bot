from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from src.classes.HandlersController import HandlersController
from src.classes.KeyboardsController import KeyboardsController, KB
from src.classes.DatabaseController import DatabaseController

from src.funcs.core import get_language_phrases, is_authorized

router = Router()

rt_controller = HandlersController()
kb_controller = KeyboardsController()

MENU_BUTTONS = get_language_phrases()["BUTTONS"]["REGISTRATION_MENU"]
REGISTER_BTN = get_language_phrases()["BUTTONS"]["REGISTER"]
INFO_BTN = get_language_phrases()["BUTTONS"]["INFO"]

start_msg = get_language_phrases()["MESSAGES"]["START_MESSAGE"]
success_msg = get_language_phrases()["MESSAGES"]["SUCCESSFULL_REGISTER"]
info_msg = get_language_phrases()["MESSAGES"]["INFO_REGISTER"]

@router.message(Command("start"))
async def register_handler(msg: Message):
       if not DatabaseController().get_user(id=msg.from_user.id):
              await msg.reply(start_msg, 
                            reply_markup=kb_controller.get_keyboard(KB.register))
       else:
              await msg.answer(success_msg, 
                     reply_markup=kb_controller.get_keyboard(KB.main))

@router.message(F.text.startswith(MENU_BUTTONS["REGISTER"]))
async def get_register(msg: Message):
       if not DatabaseController().get_user(id=msg.from_user.id):
              DatabaseController().add_user(id=msg.from_user.id, name=msg.from_user.username, date="17-09-2004", gender="Male", language=1, blood=1)
              await msg.answer(success_msg, 
                     reply_markup=kb_controller.get_keyboard(KB.main))
       else:
              await msg.answer(success_msg, 
                            reply_markup=kb_controller.get_keyboard(KB.main))

@router.message(F.text.startswith(MENU_BUTTONS["INFO"]))
async def get_info(msg: Message):
       if not DatabaseController().get_user(id=msg.from_user.id):
              await msg.answer(info_msg)
       
rt_controller.add_router(router)