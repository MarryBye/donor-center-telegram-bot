from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [
    [
        {"NOTIFICATIONS_MENU_ON": {"callback_data": "True"}},
        {"NOTIFICATIONS_MENU_OFF": {"callback_data": "False"}},
    ]
]

keyboard = Keyboard(keyboard_scheme=kb_scheme)
kb.add_keyboard(keyboard_name=KeyboardName.NOTIFICATIONS, keyboard=keyboard)
