from src.classes.Keyboards import Keyboard, KeyboardController

kb = KeyboardController()

kb_scheme = [["FEEDBACK_MENU_PHONE", "FEEDBACK_MENU_MAIL"], 
             ["BUTTON_HOME"]]

keyboard = Keyboard(keyboard=kb_scheme)
kb.add_keyboard(name=kb.FEEDBACK, keyboard=keyboard)
