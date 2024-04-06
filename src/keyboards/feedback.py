from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [[{"FEEDBACK_MENU_PHONE": {}}, {"FEEDBACK_MENU_MAIL": {}}], 
             [{"BUTTON_HOME": {}}]]

keyboard = Keyboard(keyboardScheme=kb_scheme)
kb.add_keyboard(keyboardName=KeyboardName.FEEDBACK, keyboard=keyboard)
