from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.classes.KeyboardsController import KeyboardsController, KB
from config import BUTTONS_TEXT

MENU_BUTTONS_TEXT = BUTTONS_TEXT["DONATION_MENU"]

register_on_donation = KeyboardButton(text=MENU_BUTTONS_TEXT["REGISTER"])

find_centers = KeyboardButton(text=MENU_BUTTONS_TEXT["FIND_CENTERS"])
work_time = KeyboardButton(text=MENU_BUTTONS_TEXT["WORK_TIME"])

send_results = KeyboardButton(text=MENU_BUTTONS_TEXT["SEND_RESULTS"])
information = KeyboardButton(text=MENU_BUTTONS_TEXT["INFO"])

back_to_menu = KeyboardButton(text=BUTTONS_TEXT["MENU"])

keyboard_scheme = [
    [register_on_donation],
    [find_centers, work_time],
    [send_results, information],
    [back_to_menu]
]

donation_keyboard = ReplyKeyboardMarkup(keyboard=keyboard_scheme, resize_keyboard=True)

kb_controller = KeyboardsController()
kb_controller.add_keyboard(KB.donation, donation_keyboard)