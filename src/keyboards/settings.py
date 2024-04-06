from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [
    [{"SETTINGS_MENU_NOTIFICATIONS": {}}],
    [{"SETTINGS_MENU_LANGUAGES": {}}],
    [{"BUTTON_HOME": {}}]
]

keyboard = Keyboard(keyboardScheme=kb_scheme)
kb.add_keyboard(keyboardName=KeyboardName.SETTINGS, keyboard=keyboard)