from src.classes.Keyboards import Keyboard, KeyboardController

kb = KeyboardController()

kb_scheme = [["BUTTON_HOME"]]  # [["BUTTON_HOME", "BUTTON_BACK"]]

keyboard = Keyboard(keyboard=kb_scheme)
kb.add_keyboard(name=kb.MENUBACK, keyboard=keyboard)
