from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import Union

from src.classes.Singleton import Singleton
from src.classes.DatabaseController import DatabaseController

from src.lang.languages import LANGUAGES

class Keyboard:
    def __init__(self, scheme: list):
        self.name_scheme = scheme
        self.scheme = []
        
        self.reload_for(user_id=-1)
        
    def create_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(keyboard=self.scheme, resize_keyboard=True)

    def reload_for(self, user_id: Union[int, str]):
        self.scheme = []
        for buttons_row in self.name_scheme:
            scheme_buttons_row = []
            for button in buttons_row:
                
                user_language = DatabaseController().get_user_language(user_id=user_id)
                button_text_translated = LANGUAGES[user_language]["BUTTONS"][button]
                
                scheme_buttons_row.append(KeyboardButton(text=button_text_translated))
            self.scheme.append(scheme_buttons_row)
            
        return self.create_keyboard()
            
class KeyboardController(metaclass=Singleton):
    REGISTRATION = "REGISTRATION"
    
    def __init__(self):
        self.keyboards = {}
        
    def add_keyboard(self, name: str, keyboard: Keyboard):
        self.keyboards[name] = keyboard
        
    def get_keyboard(self, name: str) -> Keyboard:
        return self.keyboards[name]
        
    
        