from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [[{"SEND_CONTACT": {"callback_data": "send_contact", "request_contact": True}}]]

keyboard = Keyboard(keyboard_scheme=kb_scheme)
kb.add_keyboard(keyboard_name=KeyboardName.MSG_SHARECONTACT, keyboard=keyboard)
