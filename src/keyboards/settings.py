from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.classes.KeyboardsController import KeyboardsController, KB
from config import BUTTONS_TEXT

MENU_BUTTONS_TEXT = BUTTONS_TEXT["SETTINGS_MENU"]

notifications = KeyboardButton(text=MENU_BUTTONS_TEXT["NOTIFICATIONS"])
security = KeyboardButton(text=MENU_BUTTONS_TEXT["SECURITY"])

back_to_menu = KeyboardButton(text=BUTTONS_TEXT["MENU"])

keyboard_scheme = [
    [notifications],
    [security],
    [back_to_menu]
]

settings_keyboard = ReplyKeyboardMarkup(keyboard=keyboard_scheme, resize_keyboard=True)

kb_controller = KeyboardsController()
kb_controller.add_keyboard(KB.settings, settings_keyboard)