from src.classes.Keyboards import Keyboard, KeyboardController

kb = KeyboardController()

kb_scheme = [
    ["LANGUAGES_MENU_UK", "LANGUAGES_MENU_EN", "LANGUAGES_MENU_RU"],
    ["LANGUAGES_MENU_DE", "LANGUAGES_MENU_CN", "LANGUAGES_MENU_FR"],
    ["BUTTON_HOME"]
]

keyboard = Keyboard(keyboard=kb_scheme)
kb.add_keyboard(name=kb.LANGUAGES, keyboard=keyboard)