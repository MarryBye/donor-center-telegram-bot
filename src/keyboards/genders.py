from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName
from src.classes.Controllers.DatabaseController import DatabaseController

kb = KeyboardController()
db = DatabaseController()

genders = db.get_genders()

kb_scheme = []

kb_scheme_row = []
for i, gender in enumerate(genders, start=0):
    kb_scheme_row.append({gender.get_gender_name(): {"callback_data": str(gender.get_id())}})
    if i % 3 == 0 or i >= len(genders) - 1:
        kb_scheme.append(kb_scheme_row)
        kb_scheme_row = []

keyboard = Keyboard(keyboard_scheme=kb_scheme)
kb.add_keyboard(keyboard_name=KeyboardName.GENDERS, keyboard=keyboard)
