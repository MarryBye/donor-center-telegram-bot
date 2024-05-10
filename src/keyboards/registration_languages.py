from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [
    [{"LANGUAGES_MENU_UK": {"callback_data": "uk-UK"}}, {"LANGUAGES_MENU_EN": {"callback_data": "en-EN"}}, {"LANGUAGES_MENU_RU": {"callback_data": "ru-RU"}}],
    [{"LANGUAGES_MENU_DE": {"callback_data": "de-DE"}}, {"LANGUAGES_MENU_CN": {"callback_data": "cn-CN"}}, {"LANGUAGES_MENU_FR": {"callback_data": "fr-FR"}}]
]

keyboard = Keyboard(keyboard_scheme=kb_scheme)
kb.add_keyboard(keyboard_name=KeyboardName.LANGUAGES_REGISTER, keyboard=keyboard)
