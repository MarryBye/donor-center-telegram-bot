from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.classes.KeyboardsController import KeyboardsController, KB
from config import BUTTONS_TEXT

MENU_BUTTONS_TEXT = BUTTONS_TEXT["FEEDBACK_MENU"]

fast_ans1 = KeyboardButton(text=MENU_BUTTONS_TEXT["FAST_ANS1"])
fast_ans2 = KeyboardButton(text=MENU_BUTTONS_TEXT["FAST_ANS2"])
fast_ans3 = KeyboardButton(text=MENU_BUTTONS_TEXT["FAST_ANS3"])
fast_ans4 = KeyboardButton(text=MENU_BUTTONS_TEXT["FAST_ANS4"])
fast_ans5 = KeyboardButton(text=MENU_BUTTONS_TEXT["FAST_ANS5"])
fast_ans6 = KeyboardButton(text=MENU_BUTTONS_TEXT["FAST_ANS6"])
need_operator = KeyboardButton(text=MENU_BUTTONS_TEXT["NEED_OPERATOR"])

back_to_menu = KeyboardButton(text=BUTTONS_TEXT["MENU"])

keyboard_scheme = [
    [fast_ans1, fast_ans2],
    [fast_ans3, fast_ans4],
    [fast_ans5, fast_ans6],
    [need_operator],
    [back_to_menu]
]

feedback_keyboard = ReplyKeyboardMarkup(keyboard=keyboard_scheme, resize_keyboard=True)

kb_controller = KeyboardsController()
kb_controller.add_keyboard(KB.feedback, feedback_keyboard)