from typing import Union
from aiogram import F

from src.classes.DatabaseController import DatabaseController

from src.lang.languages import LANGUAGES

db = DatabaseController()

def is_pressed_kb_button(key: str):
    command_variations = []
    for language in LANGUAGES:
        command_variations.append(LANGUAGES[language]["BUTTONS"][key])
    return F.text.in_(command_variations)

def message_translated(user_id: Union[int, str], key: str):
    return LANGUAGES[db.get_user_language(user_id=user_id)]["MESSAGES"][key]

def button_translated(user_id: Union[int, str], key: str):
    return LANGUAGES[db.get_user_language(user_id=user_id)]["BUTTONS"][key]