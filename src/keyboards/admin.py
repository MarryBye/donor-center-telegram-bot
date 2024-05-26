from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [[{"ADMIN_MENU_SEND_NOTIFICATIONS": {"callback_data": "send_notifications"}}],
             [{"ADMIN_MENU_GET_CLINIC_INFO": {"callback_data": "clinic_info"}}]]

keyboard = Keyboard(keyboard_scheme=kb_scheme)
kb.add_keyboard(keyboard_name=KeyboardName.EDIT_PROFILE, keyboard=keyboard)
