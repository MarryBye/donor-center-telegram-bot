from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.classes.KeyboardsController import KeyboardsController, KB
from config import BUTTONS_TEXT

MENU_BUTTONS_TEXT = BUTTONS_TEXT["REGISTRATION_MENU"]

registration_start = KeyboardButton(text=MENU_BUTTONS_TEXT["REGISTER"])
information = KeyboardButton(text=MENU_BUTTONS_TEXT["INFO"])

KEYBOARD_SCHEME = [
    [registration_start],
    [information]
]

registration_keyboard = ReplyKeyboardMarkup(keyboard=KEYBOARD_SCHEME, resize_keyboard=True)

kb_controller = KeyboardsController()
kb_controller.add_keyboard(KB.register, registration_keyboard)