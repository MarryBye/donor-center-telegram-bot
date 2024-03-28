from src.classes.Keyboards import Keyboard, KeyboardController

kb = KeyboardController()

registration_kb_scheme = [
    ["REG_MENU_REGISTER"],
    ["REG_MENU_INFO", "REG_MENU_LANGUAGES"],
]

registration_keyboard = Keyboard(keyboard=registration_kb_scheme)

kb.add_keyboard(name=kb.REGISTRATION, keyboard=registration_keyboard)