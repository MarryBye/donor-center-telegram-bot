from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from src.classes.HandlersController import HandlersController
from src.classes.KeyboardsController import KeyboardsController, KB
from config import MESSAGES_TEXT, BUTTONS_TEXT

router = Router()

rt_controller = HandlersController()
kb_controller = KeyboardsController()

MENU_BUTTONS = BUTTONS_TEXT["LANGUAGES_MENU"]
UK_BTN = MENU_BUTTONS["UK"]
EN_BTN = MENU_BUTTONS["EN"]
RU_BTN = MENU_BUTTONS["RU"]
DE_BTN = MENU_BUTTONS["DE"]
CN_BTN = MENU_BUTTONS["CN"]
FR_BTN = MENU_BUTTONS["FR"]

menuOpen_msg = MESSAGES_TEXT["MENU_OPEN"]

@router.message(F.text.startswith(UK_BTN))
async def get_register(msg: Message):
       await msg.answer(menuOpen_msg.format(UK_BTN), 
                        reply_markup=kb_controller.get_keyboard(KB.main))

@router.message(F.text.startswith(EN_BTN))
async def get_info(msg: Message):
       await msg.answer(menuOpen_msg.format(EN_BTN), 
                        reply_markup=kb_controller.get_keyboard(KB.main))
       
@router.message(F.text.startswith(RU_BTN))
async def get_info(msg: Message):
       await msg.answer(menuOpen_msg.format(RU_BTN), 
                        reply_markup=kb_controller.get_keyboard(KB.main))
       
@router.message(F.text.startswith(DE_BTN))
async def get_info(msg: Message):
       await msg.answer(menuOpen_msg.format(DE_BTN), 
                        reply_markup=kb_controller.get_keyboard(KB.main))
       
@router.message(F.text.startswith(CN_BTN))
async def get_info(msg: Message):
       await msg.answer(menuOpen_msg.format(CN_BTN), 
                        reply_markup=kb_controller.get_keyboard(KB.main))
       
@router.message(F.text.startswith(FR_BTN))
async def get_info(msg: Message):
       await msg.answer(menuOpen_msg.format(FR_BTN), 
                        reply_markup=kb_controller.get_keyboard(KB.main))
       
rt_controller.add_router(router)