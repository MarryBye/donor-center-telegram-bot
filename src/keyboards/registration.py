from src.classes.Keyboards import Keyboard, KeyboardController

registration_kb_scheme = [
    ["REG_MENU_REGISTER"],
    ["REG_MENU_INFO"]
]

registration_keyboard = Keyboard(scheme=registration_kb_scheme)
KeyboardController().add_keyboard(name=KeyboardController.REGISTRATION, keyboard=registration_keyboard)


