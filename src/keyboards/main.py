from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.classes.KeyboardsController import KeyboardsController, KB
from config import BUTTONS_TEXT

MENU_BUTTONS_TEXT = BUTTONS_TEXT["MAIN_MENU"]

donation_menu = KeyboardButton(text=MENU_BUTTONS_TEXT["DONATION"])
settings_menu = KeyboardButton(text=MENU_BUTTONS_TEXT["SETTINGS"])
feedback_menu = KeyboardButton(text=MENU_BUTTONS_TEXT["FEEDBACK"])
language_menu = KeyboardButton(text=MENU_BUTTONS_TEXT["LANGUAGES"])

keyboard_scheme = [
    [donation_menu],
    [settings_menu],
    [feedback_menu],
    [language_menu]
]

main_keyboard = ReplyKeyboardMarkup(keyboard=keyboard_scheme, resize_keyboard=True)

kb_controller = KeyboardsController()
kb_controller.add_keyboard(KB.main, main_keyboard)