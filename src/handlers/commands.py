import asyncio
import config as cfg

from re import match
from random import choice

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.classes.CRMBot import CRMBot
from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import Form, Feedback

from src.funcs.core import pressed_button, message_translate, button_translate
from src.funcs.debug_print import debug_print

bot = CRMBot()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="User commands router")


@router.message(Command("cancel"))
async def main_handler(msg: Message, state: FSMContext):

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    if await state.get_state() is not None:
        await state.clear()

        new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.MAIN, keyboard_type=KeyboardType.REPLY,
                                       language_name=user_language)
        bot_message = message_translate(message_name="CANCELLED_STATE", language_name=user_language)

        await msg.reply(text=bot_message, reply_markup=new_keyboard)

    debug_print("User", user_id, "has cancelled last command!")


@router.message(Command("notify_all"))
async def main_handler(msg: Message, state: FSMContext):
    # TODO Когда в базе данных появятся админы - добавить защиту

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    photos = None
    text = None

    if msg.photo is not None:
        photos = [photo for photo in msg.photo]
        text = msg.caption.replace("/notify_all ", "")
    else:
        text = msg.text.replace("/notify_all ", "")

    bot_message = message_translate(message_name="CANCELLED_STATE", language_name=user_language)

    for user_id in db.get_notifications_list():
        if photos is not None:
            await bot.send_photo(user_id, photo=photos[-1].file_id, caption=text)
        else:
            await bot.send_message(user_id, text)
        # Чтобы не получить рейт лимит, каждые 1 сообщение каждые 3 секунды
        await asyncio.sleep(3)

    await msg.reply(text=bot_message)

    debug_print("Admin", user_id, "has notified all users!")

@router.message(Command("admin_panel"))
async def main_handler(msg: Message, state: FSMContext):
    # TODO Когда в базе данных появятся админы - добавить защиту

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    debug_print("User", user_id, "has authorized as admin!")


hnd.add_router(router)
