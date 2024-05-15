from re import match
from aiocache import Cache

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.funcs.core import pressed_button, message_translate

from src.classes.Form import Feedback
from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType


cache = Cache()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="FEEDBACK ROUTER")


@router.message(Feedback.name)
async def process_name(msg: Message, state: FSMContext):

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    name = msg.text.strip()

    new_keyboard = kb.get_keyboard(
        keyboardName=KeyboardName.FEEDBACK,
        keyboardType=KeyboardType.REPLY,
        languageName=user_language,
    )

    bot_message = message_translate(
        message_name="FEEDBACK_AFTER_NAME_MESSAGE", language_name=user_language
    )

    if not name.isdigit():
        await state.update_data(name=name)
        await cache.set(f"user:{user_id}:name", name)
        await state.clear()
        await msg.answer(bot_message, reply_markup=new_keyboard)
    else:
        await msg.answer(
            message_translate(
                message_name="MAIL_PHONE_ERROR", language_name=user_language
            )
        )


@router.message(pressed_button(button_name="FEEDBACK_MENU_PHONE"))
async def feedback_phone_handler(msg: Message, state: FSMContext):

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    new_keyboard = kb.get_keyboard(
        keyboardName=KeyboardName.MENUBACK,
        keyboardType=KeyboardType.REPLY,
        languageName=user_language,
    )
    bot_message = message_translate(
        message_name="FEEDBACK_PHONE_MESSAGE", language_name=user_language
    )

    await state.set_state(Feedback.phone)
    await msg.answer(bot_message, reply_markup=new_keyboard)


@router.message(Feedback.phone)
async def process_phone(msg: Message, state: FSMContext):

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    phone = msg.text

    new_keyboard = kb.get_keyboard(
        keyboardName=KeyboardName.MENUBACK,
        keyboardType=KeyboardType.REPLY,
        languageName=user_language,
    )
    bot_message = message_translate(
        message_name="PHONE_SENT", language_name=user_language
    )
    try:
        if match(r"^\+?(\d{10,15})$", phone):
            await msg.answer(bot_message, reply_markup=new_keyboard)
            await state.clear()

            name = await cache.get(f"user:{user_id}:name")

            print(phone, name)

            db.add_feedback_request(user_id=user_id, note=f"Telegram: {name} | {phone}")
            print("все ок")
        else:
            await msg.answer(
                message_translate(
                    message_name="MAIL_PHONE_ERROR", language_name=user_language
                )
            )
            print("phone error")
    except Exception as e:
        await msg.answer(
            message_translate(
                message_name="MAIL_PHONE_ERROR", language_name=user_language
            )
        )
        print(f"`process_phone` ERROR:{e}")


@router.message(pressed_button(button_name="FEEDBACK_MENU_MAIL"))
async def feedback_mail_handler(msg: Message, state: FSMContext):

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    new_keyboard = kb.get_keyboard(
        keyboardName=KeyboardName.MENUBACK,
        keyboardType=KeyboardType.REPLY,
        languageName=user_language,
    )

    bot_message = message_translate(
        message_name="FEEDBACK_MAIL_MESSAGE", language_name=user_language
    )

    await state.set_state(Feedback.mail)
    await msg.answer(bot_message, reply_markup=new_keyboard)


@router.message(Feedback.mail)
async def process_phone(msg: Message, state: FSMContext):

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    mail = msg.text

    new_keyboard = kb.get_keyboard(
        keyboardName=KeyboardName.MENUBACK,
        keyboardType=KeyboardType.REPLY,
        languageName=user_language,
    )
    bot_message = message_translate(
        message_name="MAIL_SENT", language_name=user_language
    )

    if match(r"^[^@]+@[^@]+\.[^@]+$", mail):
        await msg.answer(bot_message, reply_markup=new_keyboard)
        await state.clear()

        name = await cache.get(f"user:{user_id}:name")

        print(mail, name)

        db.add_feedback_request(user_id=user_id, note=f"Telegram: {name} | {mail}")
        print("все ок")
    else:
        await msg.answer(
            message_translate(
                message_name="MAIL_PHONE_ERROR", language_name=user_language
            )
        )
        print("mail error")


hnd.add_router(router)
