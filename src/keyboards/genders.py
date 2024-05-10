from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [
    [{"MALE": {"callback_data": "MALE"}}, {"FEMALE": {"callback_data": "FEMALE"}}],
    [{"OTHER": {"callback_data": "OTHER"}}],
    [{"NODATA": {"callback_data": "NODATA"}}]
]

keyboard = Keyboard(keyboard_scheme=kb_scheme)
kb.add_keyboard(keyboard_name=KeyboardName.GENDERS, keyboard=keyboard)
