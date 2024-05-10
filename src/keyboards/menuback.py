from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [[{"BUTTON_HOME": {}}]]  # [["BUTTON_HOME", "BUTTON_BACK"]]

keyboard = Keyboard(keyboard_scheme=kb_scheme)
kb.add_keyboard(keyboard_name=KeyboardName.MENUBACK, keyboard=keyboard)
