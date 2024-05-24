from aiogram import Router
from aiogram.types import Message

from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType

from src.funcs.core import pressed_button, message_translate, language_name_to_id

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="LANGUAGES ROUTER")


@router.message(pressed_button(button_name="LANGUAGES_MENU_UK"))
async def language_handler(msg: Message):
    user_id = msg.from_user.id

    db.set_user_language(user_id=msg.from_user.id, language=language_name_to_id(language_name="uk-UK"))

    user_language = db.get_user_language(user_id=user_id)

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.MAIN, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="SUCCESFULLY_CHANGED_LANGUAGE", language_name=user_language)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


@router.message(pressed_button(button_name="LANGUAGES_MENU_EN"))
async def language_handler(msg: Message):
    user_id = msg.from_user.id

    db.set_user_language(user_id=msg.from_user.id, language=language_name_to_id(language_name="en-EN"))

    user_language = db.get_user_language(user_id=user_id)

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.MAIN, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="SUCCESFULLY_CHANGED_LANGUAGE", language_name=user_language)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


@router.message(pressed_button(button_name="LANGUAGES_MENU_RU"))
async def language_handler(msg: Message):
    user_id = msg.from_user.id

    db.set_user_language(user_id=msg.from_user.id, language=language_name_to_id(language_name="ru-RU"))

    user_language = db.get_user_language(user_id=user_id)

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.MAIN, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="SUCCESFULLY_CHANGED_LANGUAGE", language_name=user_language)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


@router.message(pressed_button(button_name="LANGUAGES_MENU_DE"))
async def language_handler(msg: Message):
    user_id = msg.from_user.id

    db.set_user_language(user_id=msg.from_user.id, language=language_name_to_id(language_name="de-DE"))

    user_language = db.get_user_language(user_id=user_id)

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.MAIN, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="SUCCESFULLY_CHANGED_LANGUAGE", language_name=user_language)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


@router.message(pressed_button(button_name="LANGUAGES_MENU_CN"))
async def language_handler(msg: Message):
    user_id = msg.from_user.id

    db.set_user_language(user_id=msg.from_user.id, language=language_name_to_id(language_name="cn-CN"))

    user_language = db.get_user_language(user_id=user_id)

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.MAIN, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="SUCCESFULLY_CHANGED_LANGUAGE", language_name=user_language)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


@router.message(pressed_button(button_name="LANGUAGES_MENU_FR"))
async def language_handler(msg: Message):
    user_id = msg.from_user.id

    db.set_user_language(user_id=msg.from_user.id, language=language_name_to_id(language_name="fr-FR"))

    user_language = db.get_user_language(user_id=user_id)

    new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.MAIN, keyboard_type=KeyboardType.REPLY,
                                   language_name=user_language)
    bot_message = message_translate(message_name="SUCCESFULLY_CHANGED_LANGUAGE", language_name=user_language)

    await msg.reply(text=bot_message, reply_markup=new_keyboard)


hnd.add_router(router)
