from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.classes.CRMBot import CRMBot
from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import ChooseNotifications

from src.funcs.core import pressed_button, message_translate, sent_callback

bot = CRMBot()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="NOTIFICATIONS ROUTER")


@router.callback_query(ChooseNotifications.choose_notification)
async def main_handler(call: CallbackQuery, state: FSMContext):

    user_id = call.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    notify_status = True if call.data == "True" else False

    db.set_user_notifications(user_id=user_id, option=notify_status)

    await state.clear()

    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    await bot.answer(
        user_id=user_id,
        text="NOTIFICATIONS_ON" if notify_status else "NOTIFICATIONS_OFF",
        keyboard_name=KeyboardName.MAIN,
        keyboard_type=KeyboardType.REPLY,
        language_name=user_language
    )

hnd.add_router(router)
