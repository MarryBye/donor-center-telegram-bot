from typing import Union
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.classes.Singleton import Singleton
from src.classes.DatabaseController import DatabaseController

from src.lang.languages import LANGUAGES

class Keyboard:
    def __init__(self, keyboard: list, needTranslation=True):
        self.name_scheme = keyboard
        self.scheme = []
        self.needTranslation = needTranslation
        
        self.reload_for(user_id=-1)
        
    def create_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(keyboard=self.scheme, resize_keyboard=True)

    def reload_for(self, user_id: Union[int, str]):
        if self.needTranslation:
            self.scheme = []
            user_language = DatabaseController().get_user_language(user_id=user_id)
            
            for buttons_row in self.name_scheme:
                scheme_buttons_row = []
                for button in buttons_row:
                
                    button_text_translated = LANGUAGES[user_language]["BUTTONS"][button]
                    
                    scheme_buttons_row.append(KeyboardButton(text=button_text_translated))
                self.scheme.append(scheme_buttons_row)
        else:
            self.scheme = self.name_scheme.copy()
            
        return self.create_keyboard()
            
class KeyboardController(metaclass=Singleton):
    MAIN = "MAIN"
    LANGUAGES = "LANGUAGES"
    SETTINGS = "SETTINGS"
    NOTIFICATIONS = "NOTIFICATIONS"
    DONATION = "DONATION"
    
    def __init__(self):
        self.keyboards = {}
        
    def add_keyboard(self, name: str, keyboard: Keyboard):
        self.keyboards[name] = keyboard
        
    def get_keyboard(self, name: str) -> Keyboard:
        return self.keyboards[name]
        
    
        