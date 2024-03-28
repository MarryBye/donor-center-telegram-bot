from src.classes.Keyboards import Keyboard, KeyboardController

kb = KeyboardController()

main_kb_scheme = [
    ["MAIN_MENU_DONATION"],
    ["MAIN_MENU_INFO"],
    ["MAIN_MENU_FEEDBACK"],
    ["MAIN_MENU_SETTINGS"]
]

main_kb = Keyboard(keyboard=main_kb_scheme)

kb.add_keyboard(name=kb.MAIN, keyboard=main_kb)