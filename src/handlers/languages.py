from aiogram import Router
from aiogram.types import Message

from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import ChooseLanguage

from src.funcs.core import pressed_button, message_translate, language_name_to_id

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="LANGUAGES ROUTER")


@router.callback_query(ChooseLanguage.chooseLanguage)
async def language_handler(msg: Message):
    pass
    # user_id = msg.from_user.id
    #
    # db.set_user_language(user_id=msg.from_user.id, language=language_name_to_id(language_name="uk-UK"))
    #
    # user_language = db.get_user_language(user_id=user_id)
    #
    # new_keyboard = kb.get_keyboard(keyboard_name=KeyboardName.MAIN, keyboard_type=KeyboardType.REPLY,
    #                                language_name=user_language)
    # bot_message = message_translate(message_name="SUCCESFULLY_CHANGED_LANGUAGE", language_name=user_language)
    #
    # await msg.reply(text=bot_message, reply_markup=new_keyboard)


hnd.add_router(router)
