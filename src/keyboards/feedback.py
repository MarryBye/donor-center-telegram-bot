from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [[{"FEEDBACK_MENU_PHONE": {}}, {"FEEDBACK_MENU_MAIL": {}}], 
             [{"BUTTON_HOME": {}}]]

keyboard = Keyboard(keyboard_scheme=kb_scheme)
kb.add_keyboard(keyboard_name=KeyboardName.FEEDBACK, keyboard=keyboard)
