import json

from src.classes.DatabaseController import DatabaseController

def is_authorized(user_id: int) -> bool:
    '''Перевірити, чи зареєстрован користувач'''
    
    return DatabaseController().get_user(user_id=user_id)
    
def get_language_phrases(user_id: int) -> dict:
    '''Отримати словник фраз чат-боту для окремого користувача виходячи з даних, які записані у БД.'''
    
    language = DatabaseController().get_user_language(user_id=user_id)[0]
    
    return json.load(open(f"src/lang/{language}.json", "r"))