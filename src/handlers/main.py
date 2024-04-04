import config as cfg

from random import choice

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController
from src.classes.Form import Form

from src.funcs.core import is_pressed_kb_button, message_translated, button_translated

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router()

@router.message(Command("start"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       
       db.set_user_notifications(user_id=user_id, option=True)
       db.set_user_language(user_id=msg.from_user.id, language=cfg.DEFAULT_LANGUAGE)
       
       new_keyboard = kb.get_keyboard(kb.MAIN).reload_for(user_id)
       bot_message = message_translated(user_id=user_id, key="START_MESSAGE")
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)

@router.message(is_pressed_kb_button("MAIN_MENU_DONATION"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       
       new_keyboard = kb.get_keyboard(kb.DONATION).reload_for(user_id)
       bot_message = message_translated(user_id=user_id, key="MENU_OPEN") % button_translated(user_id=user_id, key="MAIN_MENU_DONATION")
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)

@router.message(is_pressed_kb_button("MAIN_MENU_INFO"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       
       bot_message = message_translated(user_id=user_id, key="INFO_REGISTER")
              
       await msg.reply(text=bot_message)
       
@router.message(is_pressed_kb_button("MAIN_MENU_SETTINGS"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       
       new_keyboard = kb.get_keyboard(kb.SETTINGS).reload_for(user_id)
       bot_message = message_translated(user_id=user_id, key="MENU_OPEN") % button_translated(user_id=user_id, key="MAIN_MENU_SETTINGS")
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)
       
@router.message(is_pressed_kb_button("MAIN_MENU_FEEDBACK"))
async def feedback_handler(msg: Message, state: FSMContext):

    user_id = msg.from_user.id

    new_keyboard = kb.get_keyboard(kb.FEEDBACK).reload_for(user_id)
    bot_message = message_translated(
        user_id=user_id, key="FEEDBACK_MENU_OPEN"
    ) % button_translated(user_id=user_id, key="MAIN_MENU_FEEDBACK")

    await msg.reply(bot_message, reply_markup=new_keyboard)

    # TODO: если имя есть в бд, то пропустить шаг с ним
    # if not name_in_db:

    await state.set_state(Feedback.name)
    await msg.answer(
        message_translated(user_id, key="NAME_SENT"),
        reply_markup=kb.get_keyboard(kb.MENUBACK).reload_for(user_id),
    )


hnd.add_router(router)
