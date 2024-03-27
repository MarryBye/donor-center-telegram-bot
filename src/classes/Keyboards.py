from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import Union

from src.classes.Singleton import Singleton
from src.funcs.core import get_language_phrases

class Keyboard:
    def __init__(self, scheme: list):
        self.name_scheme = scheme
        self.scheme = []
        
        self.reload_for(user_id=-1)
        
    def get_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(keyboard=self.scheme, resize_keyboard=True)

    def reload_for(self, user_id: Union[int, str]):
        self.scheme = []
        for buttons_row in self.name_scheme:
            scheme_buttons_row = []
            for button in buttons_row:
                scheme_buttons_row.append(KeyboardButton(text=get_language_phrases(user_id=user_id)["BUTTONS"][button]))
            self.scheme.append(scheme_buttons_row)
            
class KeyboardController(metaclass=Singleton):
    REGISTRATION = "REGISTRATION"
    
    def __init__(self):
        self.keyboards = {}
        
    def add_keyboard(self, name: str, keyboard: Keyboard):
        self.keyboards[name] = keyboard
        
    def get_keyboard(self, name: str) -> Keyboard:
        return self.keyboards[name].get_keyboard()
        
    
        