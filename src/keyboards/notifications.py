from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [
    [{"NOTIFICATIONS_MENU_ON": {}}, {"NOTIFICATIONS_MENU_OFF": {}}],
    [{"BUTTON_HOME": {}}]
]

keyboard = Keyboard(keyboardScheme=kb_scheme)
kb.add_keyboard(keyboardName=KeyboardName.NOTIFICATIONS, keyboard=keyboard)