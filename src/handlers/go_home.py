from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.CRMBot import CRMBot
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.funcs.core import button_translate, message_translate, pressed_button

bot = CRMBot()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="GO_HOME ROUTER")


@router.message(pressed_button(button_name="BUTTON_HOME"))
async def main_handler(msg: Message, state: FSMContext):
    await state.clear()

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    donor = db.get_donor(telegram_id=user_id)

    if donor:
        bot_message = message_translate(
            message_name="MENU_OPEN", language_name=user_language
        ) % button_translate(button_name="BUTTON_HOME", language_name=user_language)

        await bot.answer(
            user_id=user_id,
            text=bot_message,
            keyboard_name=KeyboardName.MAIN,
            keyboard_type=KeyboardType.REPLY,
            language_name=user_language,
            need_translation=False,
        )


hnd.add_router(router)
