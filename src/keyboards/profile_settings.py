from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [
    [{"EDIT_PROFILE_NAME": {"callback_data": "edit_name"}}],
    [{"EDIT_PROFILE_NUMBER": {"callback_data": "edit_number"}}],
    [{"EDIT_PROFILE_BIRTHDATE": {"callback_data": "edit_bdate"}}],
    [{"EDIT_PROFILE_GENDER": {"callback_data": "edit_gender"}}],
    [{"EDIT_PROFILE_EMAIL": {"callback_data": "edit_email"}}]
]

keyboard = Keyboard(keyboard_scheme=kb_scheme)
kb.add_keyboard(keyboard_name=KeyboardName.PROFILE_SETTINGS, keyboard=keyboard)
