from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [[{"ADMIN_MENU_SEND_NOTIFICATIONS": {}}],
             [{"ADMIN_MENU_GET_CLINIC_INFO": {}}],
             [{"ADMIN_MENU_SET_STATUS": {}}],
             [{"ADMIN_UPDATE_BLOOD": {}}]]

keyboard = Keyboard(keyboard_scheme=kb_scheme)
kb.add_keyboard(keyboard_name=KeyboardName.ADMIN, keyboard=keyboard)
