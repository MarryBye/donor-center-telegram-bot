from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [
    [{"MAIN_MENU_DONATION": {}}],
    [{"MAIN_MENU_INFO": {}}],
    [{"MAIN_MENU_FEEDBACK": {}}],
    [{"MAIN_MENU_SETTINGS": {}}]
]

keyboard = Keyboard(keyboardScheme=kb_scheme)
kb.add_keyboard(keyboardName=KeyboardName.MAIN, keyboard=keyboard)