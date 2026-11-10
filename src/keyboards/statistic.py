from src.classes.Keyboards import Keyboard, KeyboardController, KeyboardName

kb = KeyboardController()

kb_scheme = [
    [
        {"RHESUS +": {"callback_data": "rhesus_plus"}},
        {"RHESUS -": {"callback_data": "rhesus_minus"}},
    ],
]

keyboard = Keyboard(keyboard_scheme=kb_scheme)
kb.add_keyboard(keyboard_name=KeyboardName.STATISTIC, keyboard=keyboard)
