from src.classes.Keyboards import Keyboard, KeyboardController

kb = KeyboardController()

kb_scheme = [
    ["SETTINGS_MENU_NOTIFICATIONS"],
    ["SETTINGS_MENU_LANGUAGES"],
    ["BUTTON_HOME"]
]

keyboard = Keyboard(keyboard=kb_scheme)
kb.add_keyboard(name=kb.SETTINGS, keyboard=keyboard)