from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [[{"BUTTON_HOME": {}}]]  # [["BUTTON_HOME", "BUTTON_BACK"]]

keyboard = Keyboard(keyboardScheme=kb_scheme)
kb.add_keyboard(keyboardName=KeyboardName.MENUBACK, keyboard=keyboard)
