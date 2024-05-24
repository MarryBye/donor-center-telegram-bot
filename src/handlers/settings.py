from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.classes.CRMBot import CRMBot
from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import ChooseLanguage, ChooseNotifications

from src.funcs.core import pressed_button, message_translate, button_translate

bot = CRMBot()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="SETTINGS ROUTER")


@router.message(pressed_button(button_name="SETTINGS_MENU_NOTIFICATIONS"))
async def main_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    await state.set_state(ChooseNotifications.choose_notification)

    text = message_translate("MENU_OPEN", language_name=user_language) % button_translate(button_name="SETTINGS_MENU_NOTIFICATIONS", language_name=user_language)

    await bot.answer(
        user_id=user_id,
        text=text,
        keyboard_name=KeyboardName.NOTIFICATIONS,
        keyboard_type=KeyboardType.INLINE,
        language_name=user_language,
        need_translation=False
    )


@router.message(pressed_button(button_name="SETTINGS_MENU_LANGUAGES"))
async def main_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    await state.set_state(ChooseLanguage.choose_language)

    text = message_translate("MENU_OPEN", language_name=user_language) % button_translate(button_name="SETTINGS_MENU_NOTIFICATIONS", language_name=user_language)

    await bot.answer(
        user_id=user_id,
        text=text,
        keyboard_name=KeyboardName.LANGUAGES,
        keyboard_type=KeyboardType.INLINE,
        language_name=user_language,
        need_translation=False
    )


hnd.add_router(router)
