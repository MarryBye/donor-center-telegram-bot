import config as cfg

from random import choice

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import Form, Feedback

from src.funcs.core import pressed_button, message_translate, button_translate

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="MAIN ROUTER")


@router.message(pressed_button(button_name="MAIN_MENU_DONATION"))
async def main_handler(msg: Message):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.DONATION, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="MENU_OPEN", language_name=user_language) % button_translate(
        button_name="MAIN_MENU_DONATION", language_name=user_language)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


@router.message(pressed_button(button_name="MAIN_MENU_INFO"))
async def main_handler(msg: Message):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    bot_message = message_translate(message_name="INFO_REGISTER", language_name=user_language)

    await msg.reply(text=bot_message)


@router.message(pressed_button(button_name="MAIN_MENU_SETTINGS"))
async def main_handler(msg: Message):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.SETTINGS, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="MENU_OPEN", language_name=user_language) % button_translate(
        button_name="MAIN_MENU_DONATION", language_name=user_language)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


@router.message(pressed_button(button_name="MAIN_MENU_FEEDBACK"))
async def feedback_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    if db.get_donor_by(telegram_id=user_id):

        new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.FEEDBACK, keyboard_type=KeyboardType.REPLY,
                                       language_name=user_language)
        bot_message = message_translate(message_name="FEEDBACK_MENU_OPEN",
                                        language_name=user_language) % button_translate(
            button_name="MAIN_MENU_FEEDBACK", language_name=user_language)

        await msg.reply(bot_message, reply_markup=new_keyboard)

    else:
        await state.set_state(Feedback.name)

        new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.MENUBACK, keyboard_type=KeyboardType.REPLY,
                                       language_name=user_language)
        bot_message = message_translate(message_name="NAME_SENT", language_name=user_language)

        await msg.answer(bot_message, reply_markup=new_keyboard)
        
@router.message(pressed_button(button_name="MAIN_MENU_PROFILE"))
async def profile_handler(msg: Message):
    genders = {i: j for i, j in cfg.GENDERS}

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    donor = db.get_donor_by(telegram_id=user_id)

    if donor:
        gender = donor.get_gender()
        name = donor.get_name()
        phone = donor.get_number()
        bdate = donor.get_birthdate()
        gender = button_translate(
            button_name=genders[gender], language_name=user_language
        )

        bot_message = message_translate("PROFILE", language_name=user_language) % (
            name,
            phone,
            bdate,
            gender,
        )

        keyboard = kb.get_keyboard(
            keyboard_name=KeyboardName.EDIT_PROFILE,
            keyboard_type=KeyboardType.INLINE,
            language_name=user_language,
        )
        await msg.answer(bot_message, reply_markup=keyboard)


@router.message(pressed_button(button_name="MAIN_MENU_EVENTS"))
async def events_and_promo_handler(msg):
    # events = db.get_events()
    ...


hnd.add_router(router)
