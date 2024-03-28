from src.classes.Keyboards import Keyboard, KeyboardController

kb = KeyboardController()

kb_scheme = [
    ["MAIN_MENU_DONATION"],
    ["MAIN_MENU_INFO"],
    ["MAIN_MENU_FEEDBACK"],
    ["MAIN_MENU_SETTINGS"]
]

keyboard = Keyboard(keyboard=kb_scheme)
kb.add_keyboard(name=kb.MAIN, keyboard=keyboard)