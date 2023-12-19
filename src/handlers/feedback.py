from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from src.classes.HandlersController import HandlersController
from src.classes.KeyboardsController import KeyboardsController, KB
from config import MESSAGES_TEXT, BUTTONS_TEXT

router = Router()

rt_controller = HandlersController()
kb_controller = KeyboardsController()

MENU_BUTTONS = BUTTONS_TEXT["FEEDBACK_MENU"]
FAST1_BTN = MENU_BUTTONS["FAST_ANS1"]
FAST2_BTN = MENU_BUTTONS["FAST_ANS2"]
FAST3_BTN = MENU_BUTTONS["FAST_ANS3"]
FAST4_BTN = MENU_BUTTONS["FAST_ANS4"]
FAST5_BTN = MENU_BUTTONS["FAST_ANS5"]
FAST6_BTN = MENU_BUTTONS["FAST_ANS6"]
OPERATOR_BTN = MENU_BUTTONS["NEED_OPERATOR"]

menuOpen_msg = MESSAGES_TEXT["MENU_OPEN"]

@router.message(F.text.startswith(FAST1_BTN))
async def get_register(msg: Message):
       await msg.answer(menuOpen_msg.format(FAST1_BTN))

@router.message(F.text.startswith(FAST2_BTN))
async def get_info(msg: Message):
       await msg.answer(menuOpen_msg.format(FAST2_BTN))
       
@router.message(F.text.startswith(FAST3_BTN))
async def get_info(msg: Message):
       await msg.answer(menuOpen_msg.format(FAST3_BTN))
       
@router.message(F.text.startswith(FAST4_BTN))
async def get_info(msg: Message):
       await msg.answer(menuOpen_msg.format(FAST4_BTN))
       
@router.message(F.text.startswith(FAST5_BTN))
async def get_info(msg: Message):
       await msg.answer(menuOpen_msg.format(FAST5_BTN))
       
@router.message(F.text.startswith(FAST6_BTN))
async def get_info(msg: Message):
       await msg.answer(menuOpen_msg.format(FAST6_BTN))
       
@router.message(F.text.startswith(OPERATOR_BTN))
async def get_info(msg: Message):
       await msg.answer(menuOpen_msg.format(OPERATOR_BTN))
       
rt_controller.add_router(router)