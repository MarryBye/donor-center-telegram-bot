from src.classes.Keyboards import Keyboard, KeyboardController

kb = KeyboardController()

kb_scheme = [
    ["NOTIFICATIONS_MENU_ON", "NOTIFICATIONS_MENU_OFF"],
    ["BUTTON_HOME"]
]

keyboard = Keyboard(keyboard=kb_scheme)
kb.add_keyboard(name=kb.NOTIFICATIONS, keyboard=keyboard)