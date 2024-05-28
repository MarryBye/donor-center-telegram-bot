import config as cfg

from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from src.classes.CRMBot import CRMBot
from src.classes.Form import Feedback
from src.classes.Controllers.NewsController import NewsDatabase
from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.Controllers.BloodController import BloodController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType

from src.funcs.core import pressed_button, message_translate, button_translate

bot = CRMBot()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()
bc = BloodController()

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

    if db.get_donor(telegram_id=user_id):
        await state.set_state(Feedback.name)

        new_keyboard = kb.get_keyboard(
            keyboard_name=KeyboardName.MENUBACK,
            keyboard_type=KeyboardType.REPLY,
            language_name=user_language,
        )
        bot_message = message_translate(
            message_name="NAME_SENT", language_name=user_language
        )

        await msg.answer(bot_message, reply_markup=new_keyboard)


@router.message(pressed_button(button_name="MAIN_MENU_EVENTS"))
async def events_and_promo_handler(msg: Message):
    nb = NewsDatabase()

    news_list = nb.get_news(limit=5)
    formatted_text = nb.format_news_for_telegram(news_list)

    await msg.answer(
        formatted_text,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.message(pressed_button(button_name="MAIN_MENU_PROFILE"))
async def profile_handler(msg: Message):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    donor = db.get_donor(telegram_id=user_id)

    if donor:
        gender = donor.get_gender()
        name = donor.get_name()
        phone = donor.get_telephone()
        bdate = donor.get_birthdate()
        email = donor.get_email()
        gender = button_translate(
            button_name=gender.get_gender_name(), language_name=user_language
        )

        bot_message = message_translate("PROFILE", language_name=user_language) % (
            name,
            phone.get_number(),
            email,
            bdate.strftime("%d.%m.%Y"),
            gender,
        )

        keyboard = kb.get_keyboard(
            keyboard_name=KeyboardName.EDIT_PROFILE,
            keyboard_type=KeyboardType.INLINE,
            language_name=user_language,
        )
        await msg.answer(bot_message, reply_markup=keyboard)


@router.message(pressed_button(button_name="MAIN_MENU_STAT"))
async def stat_handler(msg: Message):
    user_id = msg.from_user.id
    lang = db.get_user_language(user_id=user_id)

    appointments = db.get_all_appointments(need_status="1") or 0
    
    if isinstance(appointments, list):
        appointments = len(appointments)
    else:
        appointments = 1

    A = bc.get("A", "+", "list") or 0
    B = bc.get("B", "+", "list") or 0
    AB = bc.get("AB", "+", "list") or 0
    O = bc.get("O", "+", "list") or 0

    message = message_translate("STAT_MESSAGE", lang) % (
        appointments, "RH\+", A, B, AB, O
    )

    keyboard = kb.get_keyboard(
        keyboard_name=KeyboardName.STATISTIC,
        keyboard_type=KeyboardType.INLINE,
        language_name=lang,
    )
    
    await msg.answer(message, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN_V2)

hnd.add_router(router)
