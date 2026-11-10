from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()
db = DatabaseController()

languages = db.get_languages()

kb_scheme = []

kb_scheme_row = []
for i, language in enumerate(languages, start=0):
    kb_scheme_row.append({language.get_lang_name(): {"callback_data": str(language.get_id())}})
    if i % 3 == 0 or i >= len(languages) - 1:
        kb_scheme.append(kb_scheme_row)
        kb_scheme_row = []

keyboard = Keyboard(keyboard_scheme=kb_scheme)
kb.add_keyboard(keyboard_name=KeyboardName.LANGUAGES_REGISTER, keyboard=keyboard)
