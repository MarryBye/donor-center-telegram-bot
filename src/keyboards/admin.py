from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [[{"ADMIN_MENU_SEND_NOTIFICATIONS": {}}],
             [{"ADMIN_MENU_GET_CLINIC_INFO": {}}]]

keyboard = Keyboard(keyboard_scheme=kb_scheme)
kb.add_keyboard(keyboard_name=KeyboardName.ADMIN, keyboard=keyboard)
