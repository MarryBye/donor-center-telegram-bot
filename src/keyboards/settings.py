from src.classes.Keyboards import Keyboard, KeyboardController

kb = KeyboardController()

kb_scheme = [
    ["SETTINGS_MENU_NOTIFICATIONS"],
    ["SETTINGS_MENU_SECURITY"],
    ["SETTINGS_MENU_LANGUAGES"],
    ["BUTTON_BACK"]
]

keyboard = Keyboard(keyboard=kb_scheme)
kb.add_keyboard(name=kb.SETTINGS, keyboard=keyboard)