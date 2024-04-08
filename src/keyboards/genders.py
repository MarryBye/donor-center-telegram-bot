from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [
    [{"MALE": {}}, {"FEMALE": {}}],
    [{"OTHER": {}}],
    [{"NODATA": {}}]
]

keyboard = Keyboard(keyboardScheme=kb_scheme)
kb.add_keyboard(keyboardName=KeyboardName.GENDERS, keyboard=keyboard)