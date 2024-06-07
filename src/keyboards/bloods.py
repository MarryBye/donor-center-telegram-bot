from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName
from src.classes.Controllers.DatabaseController import DatabaseController

kb = KeyboardController()
db = DatabaseController()

bloods = db.get_bloods()

kb_scheme = []

kb_scheme_row = []
for i, blood in enumerate(bloods, start=0):
    kb_scheme_row.append({blood.get_blood_and_comp_name(): {"callback_data": str(blood.get_id())}})
    if i % 3 == 0 or i >= len(bloods) - 1:
        kb_scheme.append(kb_scheme_row)
        kb_scheme_row = []

keyboard = Keyboard(keyboard_scheme=kb_scheme)
kb.add_keyboard(keyboard_name=KeyboardName.BLOODS, keyboard=keyboard)