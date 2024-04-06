from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [
    [{"SEND_CONTACT": {"callback_data": "send_contact", "request_contact": True}}],
    [{"BUTTON_HOME": {}}]
]

keyboard = Keyboard(keyboardScheme=kb_scheme)
kb.add_keyboard(keyboardName=KeyboardName.MSG_SHARECONTACT, keyboard=keyboard)