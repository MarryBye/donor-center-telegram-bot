from re import match

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode

from src.classes.CRMBot import CRMBot
from src.classes.Form import UserSettings
from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.Controllers.BloodController import BloodController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType

from src.funcs.core import message_translate, gender_name_to_id


bot = CRMBot()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()
bc = BloodController()

router = Router(name="STATISTIC ROUTER")


@router.callback_query(lambda q: q.data == "rhesus_plus")
async def positive_rhesus(call: CallbackQuery):
    user_id = call.from_user.id
    lang = db.get_user_language(user_id=user_id)

    appointments = db.get_all_appointments(need_status="1") or 0
    
    if isinstance(appointments, list):
        appointments = len(appointments)
    else:
        appointments = 1

    rh = "+"

    A = bc.get("A", rh, "list") or 0
    B = bc.get("B", rh, "list") or 0
    AB = bc.get("AB", rh, "list") or 0
    O = bc.get("O", rh, "list") or 0

    message = message_translate("STAT_MESSAGE", lang) % (
        appointments, f"RH\{rh}", A, B, AB, O,
    )

    keyboard = kb.get_keyboard(
        keyboard_name=KeyboardName.STATISTIC,
        keyboard_type=KeyboardType.INLINE,
        language_name=lang,
    )
    await bot.answer_callback_query(call.id)

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=message,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(lambda q: q.data == "rhesus_minus")
async def negative_rhesus(call: CallbackQuery):
    user_id = call.from_user.id
    lang = db.get_user_language(user_id=user_id)

    appointments = db.get_all_appointments(need_status="1") or 0
    
    if isinstance(appointments, list):
        appointments = len(appointments)
    else:
        appointments = 1
        
    rh = "-"

    A = bc.get("A", rh, "list") or 0
    B = bc.get("B", rh, "list") or 0
    AB = bc.get("AB", rh, "list") or 0
    O = bc.get("O", rh, "list") or 0

    message = message_translate("STAT_MESSAGE", lang) % (
        appointments, f"RH\{rh}", A, B, AB, O,
    )

    keyboard = kb.get_keyboard(
        keyboard_name=KeyboardName.STATISTIC,
        keyboard_type=KeyboardType.INLINE,
        language_name=lang,
    )
    await bot.answer_callback_query(call.id)

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=message,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


hnd.add_router(router)
