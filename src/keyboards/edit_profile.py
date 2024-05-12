from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [[{"EDIT_PROFILE": {"callback_data": "edit_profile"}}]]

keyboard = Keyboard(keyboard_scheme=kb_scheme)
kb.add_keyboard(keyboard_name=KeyboardName.EDIT_PROFILE, keyboard=keyboard)
