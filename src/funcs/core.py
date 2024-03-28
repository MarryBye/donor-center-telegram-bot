from aiogram import F
from src.lang.languages import LANGUAGES

def is_pressed_kb_button(key: str) -> F:
    command_variations = []
    for language in LANGUAGES:
        command_variations.append(LANGUAGES[language]["BUTTONS"][key])
    return F.text.in_(command_variations)