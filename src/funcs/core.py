import json

from src.classes.DatabaseController import DatabaseController
from src.lang.languages import LANGUAGES

def is_authorized(user_id: int) -> bool:
    '''Перевірити, чи зареєстрован користувач'''
    
    return DatabaseController().get_user(user_id=user_id)
    
def get_language(user_id: int) -> dict:
    '''Отримати словник фраз чат-боту для окремого користувача виходячи з даних, які записані у БД.'''
    
    return DatabaseController().get_user_language(user_id=user_id)[0]

def get_multilang_button(key: str) -> list:
    command_variations = []
    for language in LANGUAGES:
        command_variations.append(LANGUAGES[language]["BUTTONS"][key])
    return command_variations