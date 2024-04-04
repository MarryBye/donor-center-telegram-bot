from src.classes.Keyboards import Keyboard, KeyboardController

kb = KeyboardController()

kb_scheme = [
    ["DONATION_MENU_REGISTER", "DONATION_MENU_HISTORY"],
    ["DONATION_MENU_FIND_CENTER", "DONATION_MENU_WORKTIME"],
    ["BUTTON_HOME"]
]

keyboard = Keyboard(keyboard=kb_scheme)
kb.add_keyboard(name=kb.DONATION, keyboard=keyboard)