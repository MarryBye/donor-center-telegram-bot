from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [
    [{"MALE": {}}, {"FEMALE": {}}],
    [{"OTHER": {}}],
    [{"NODATA": {}}]
]

keyboard = Keyboard(keyboard_scheme=kb_scheme)
kb.add_keyboard(keyboard_name=KeyboardName.GENDERS, keyboard=keyboard)
