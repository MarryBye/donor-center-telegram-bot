from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.classes.Keyboards import Keyboard

registration_kb_scheme = [
    ["REG_MENU_REGISTER"],
    ["REG_MENU_INFO"]
]

registration_keyboard = Keyboard(scheme=registration_kb_scheme)
