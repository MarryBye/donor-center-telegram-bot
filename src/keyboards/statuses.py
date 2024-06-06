from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName
from src.classes.Controllers.DatabaseController import DatabaseController

kb = KeyboardController()
db = DatabaseController()

statuses = db.get_statuses()

kb_scheme = []

kb_scheme_row = []
for i, status in enumerate(statuses, start=0):
    kb_scheme_row.append({status.get_name_status(): {"callback_data": str(status.get_id())}})
    if i % 3 == 0 or i >= len(statuses) - 1:
        kb_scheme.append(kb_scheme_row)
        kb_scheme_row = []

keyboard = Keyboard(keyboard_scheme=kb_scheme, need_translation=False)
kb.add_keyboard(keyboard_name=KeyboardName.STATUSES, keyboard=keyboard)
