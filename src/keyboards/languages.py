from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.classes.KeyboardsController import KeyboardsController, KB
from config import BUTTONS_TEXT

MENU_BUTTONS_TEXT = BUTTONS_TEXT["LANGUAGES_MENU"]

ukr_lang = KeyboardButton(text=MENU_BUTTONS_TEXT["UK"])
eng_lang = KeyboardButton(text=MENU_BUTTONS_TEXT["EN"])
rus_lang = KeyboardButton(text=MENU_BUTTONS_TEXT["RU"])
deh_lang = KeyboardButton(text=MENU_BUTTONS_TEXT["DE"])
chn_lang = KeyboardButton(text=MENU_BUTTONS_TEXT["CN"])
fr_lang = KeyboardButton(text=MENU_BUTTONS_TEXT["FR"])

back_to_menu = KeyboardButton(text=BUTTONS_TEXT["MENU"])

keyboard_scheme = [
    [ukr_lang, eng_lang],
    [rus_lang, deh_lang],
    [chn_lang, fr_lang],
    [back_to_menu]
]

language_keyboard = ReplyKeyboardMarkup(keyboard=keyboard_scheme, resize_keyboard=True)

kb_controller = KeyboardsController()
kb_controller.add_keyboard(KB.languages, language_keyboard)