from src.classes.DatabaseController import DatabaseController

def is_authorized(id: int) -> bool:
    '''Перевірити, чи зареєстрован користувач'''
    
    return DatabaseController().get_user(id=id)
    
def get_language_phrases(id: int) -> dict:
    '''Отримати словник фраз чат-боту для окремого користувача виходячи з даних, які записані у БД.'''
    
    language = DatabaseController().get_user_language(id=id)[0]
    
    return open(f"{language}.json", "r")