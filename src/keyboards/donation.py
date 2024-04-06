from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [
    [{"DONATION_MENU_REGISTER": {}}, {"DONATION_MENU_HISTORY": {}}],
    [{"DONATION_MENU_FIND_CENTER": {}}],
    [{"BUTTON_HOME": {}}]
]

keyboard = Keyboard(keyboardScheme=kb_scheme)
kb.add_keyboard(keyboardName=KeyboardName.DONATION, keyboard=keyboard)