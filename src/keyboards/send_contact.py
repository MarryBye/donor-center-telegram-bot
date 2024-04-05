from src.classes.Keyboards import Keyboard, KeyboardController, MessageKeyboard

kb = KeyboardController()

kb_scheme = [
    [{"SEND_CONTACT": {"callback": "send_contact", "request_contact": True}}]
]

keyboard = MessageKeyboard(keyboard=kb_scheme)
kb.add_keyboard(name=kb.MSG_SHARECONTACT, keyboard=keyboard)