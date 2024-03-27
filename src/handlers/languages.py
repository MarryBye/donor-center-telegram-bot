from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.KeyboardsController import KeyboardsController, KB

from src.funcs.core import get_language_phrases

router = Router()

rt_controller = HandlersController()
kb_controller = KeyboardsController()

UK_BTN = get_language_phrases()["LANGUAGES_MENU"]["UK"]
EN_BTN = get_language_phrases()["LANGUAGES_MENU"]["EN"]
RU_BTN = get_language_phrases()["LANGUAGES_MENU"]["RU"]
DE_BTN = get_language_phrases()["LANGUAGES_MENU"]["DE"]
CN_BTN = get_language_phrases()["LANGUAGES_MENU"]["CN"]
FR_BTN = get_language_phrases()["LANGUAGES_MENU"]["FR"]

menuOpen_msg = get_language_phrases()["MESSAGES"]["MENU_OPEN"]

@router.message(F.text.startswith(UK_BTN))
async def set_ukrainian(msg: Message):
       
       DatabaseController().set_user_language(id=msg.from_user.id, language_ID=6)
       
       await msg.answer(menuOpen_msg.format(UK_BTN), 
                        reply_markup=kb_controller.get_keyboard(KB.main))

@router.message(F.text.startswith(EN_BTN))
async def set_english(msg: Message):
       
       DatabaseController().set_user_language(id=msg.from_user.id, language_ID=3)
              
       await msg.answer(menuOpen_msg.format(EN_BTN), 
                        reply_markup=kb_controller.get_keyboard(KB.main))
       
@router.message(F.text.startswith(RU_BTN))
async def set_russian(msg: Message):
       
       DatabaseController().set_user_language(id=msg.from_user.id, language_ID=5)
              
       await msg.answer(menuOpen_msg.format(RU_BTN), 
                        reply_markup=kb_controller.get_keyboard(KB.main))
       
@router.message(F.text.startswith(DE_BTN))
async def set_deutsch(msg: Message):
       
       DatabaseController().set_user_language(id=msg.from_user.id, language_ID=2)
              
       await msg.answer(menuOpen_msg.format(DE_BTN), 
                        reply_markup=kb_controller.get_keyboard(KB.main))
       
@router.message(F.text.startswith(CN_BTN))
async def set_chinese(msg: Message):
       
       DatabaseController().set_user_language(id=msg.from_user.id, language_ID=1)
              
       await msg.answer(menuOpen_msg.format(CN_BTN), 
                        reply_markup=kb_controller.get_keyboard(KB.main))
       
@router.message(F.text.startswith(FR_BTN))
async def set_france(msg: Message):
       
       DatabaseController().set_user_language(id=msg.from_user.id, language_ID=4)
       
       await msg.answer(menuOpen_msg.format(FR_BTN), 
                        reply_markup=kb_controller.get_keyboard(KB.main))
       
rt_controller.add_router(router)