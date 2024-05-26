import config as cfg

from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from src.classes.CRMBot import CRMBot
from src.classes.Form import Feedback
from src.classes.Controllers.NewsController import NewsDatabase
from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType

from src.funcs.core import pressed_button, message_translate, button_translate

bot = CRMBot()

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

    if db.get_donor(telegram_id=user_id):

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
        
@router.message(pressed_button(button_name="MAIN_MENU_EVENTS"))
async def events_and_promo_handler(msg: Message):
    nb = NewsDatabase()

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    news_list = nb.fetch_news(limit=5)

    text = nb.format_news_for_telegram(news_list, lang=user_language) or "."

    await bot.answer(
        user_id=user_id,
        text=text,
        keyboard_name=KeyboardName.MAIN,
        keyboard_type=KeyboardType.REPLY,
        language_name=user_language,
        need_translation=False
    )


@router.message(pressed_button(button_name="MAIN_MENU_PROFILE"))
async def profile_handler(msg: Message):
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    donor = db.get_donor(telegram_id=user_id)

    if donor:
        gender = donor.get_gender()
        name = donor.get_name()
        phone = donor.get_telephone().get_number()
        bdate = donor.get_birthdate()
        gender = donor.get_gender().get_gender_name()

        bot_message = message_translate("PROFILE", language_name=user_language) % (
            name,
            phone,
            bdate.strftime("%d-%m-%Y"),
            button_translate(button_name=gender, language_name=user_language),
        )

        keyboard = kb.get_keyboard(
            keyboard_name=KeyboardName.EDIT_PROFILE,
            keyboard_type=KeyboardType.INLINE,
            language_name=user_language,
        )
        await msg.answer(bot_message, reply_markup=keyboard)

hnd.add_router(router)
