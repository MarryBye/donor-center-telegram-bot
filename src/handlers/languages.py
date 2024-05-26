from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.classes.CRMBot import CRMBot
from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import ChooseLanguage

from src.funcs.core import pressed_button, message_translate, language_name_to_id

bot = CRMBot()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="LANGUAGES ROUTER")


@router.callback_query(ChooseLanguage.choose_language)
async def language_handler(call: CallbackQuery, state: FSMContext):

    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    language = db.get_language(db_id=call.data)

    db.set_user_language(user_id=user_id, language=language.get_lang_name())

    await state.clear()

    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    await bot.answer(
        user_id=user_id,
        text="SUCCESFULLY_CHANGED_LANGUAGE",
        keyboard_name=KeyboardName.MAIN,
        keyboard_type=KeyboardType.REPLY,
        language_name=language.get_lang_name()
    )


hnd.add_router(router)
