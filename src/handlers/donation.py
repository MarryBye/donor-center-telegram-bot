from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from src.classes.HandlersController import HandlersController
from src.classes.KeyboardsController import KeyboardsController, KB
from config import MESSAGES_TEXT, BUTTONS_TEXT

router = Router()

rt_controller = HandlersController()
kb_controller = KeyboardsController()

MENU_BUTTONS = BUTTONS_TEXT["DONATION_MENU"]
REG_BTN = MENU_BUTTONS["REGISTER"]
FIND_BTN = MENU_BUTTONS["FIND_CENTERS"]
WORK_BTN = MENU_BUTTONS["WORK_TIME"]
SEND_BTN = MENU_BUTTONS["SEND_RESULTS"]
INFO_BTN = MENU_BUTTONS["INFO"]

menuOpen_msg = MESSAGES_TEXT["MENU_OPEN"]

@router.message(F.text.startswith(REG_BTN))
async def get_register(msg: Message):
       await msg.answer(menuOpen_msg.format(REG_BTN))

@router.message(F.text.startswith(FIND_BTN))
async def get_register(msg: Message):
       await msg.answer(menuOpen_msg.format(FIND_BTN))

@router.message(F.text.startswith(WORK_BTN))
async def get_register(msg: Message):
       await msg.answer(menuOpen_msg.format(WORK_BTN))

@router.message(F.text.startswith(SEND_BTN))
async def get_register(msg: Message):
       await msg.answer(menuOpen_msg.format(SEND_BTN))

@router.message(F.text.startswith(INFO_BTN))
async def get_register(msg: Message):
       await msg.answer(menuOpen_msg.format(INFO_BTN))
       
rt_controller.add_router(router)