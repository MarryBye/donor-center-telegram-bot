from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [
    [{"GENDER_MALE": {}}, {"GENDER_FEMALE": {}}],
    [{"GENDER_OTHER": {}}],
    [{"GENDER_NODATA": {}}]
]

keyboard = Keyboard(keyboardScheme=kb_scheme)
kb.add_keyboard(keyboardName=KeyboardName.GENDERS, keyboard=keyboard)