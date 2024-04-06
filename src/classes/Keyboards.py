from typing import Union
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

from src.classes.Singleton import Singleton
from src.lang.languages import LANGUAGES

class KeyboardType:
    INLINE = 0
    REPLY = 1
    
class KeyboardName:
    MAIN = "MAIN"
    LANGUAGES = "LANGUAGES"
    SETTINGS = "SETTINGS"
    NOTIFICATIONS = "NOTIFICATIONS"
    DONATION = "DONATION"
    FEEDBACK = "FEEDBACK"
    MENUBACK = "MENUBACK"
    MSG_SHARECONTACT = "MSG_SHARECONTACT"

class Keyboard:
    def __init__(self, keyboardScheme: list[dict[str, dict]], needTranslation=True):
        self.__nameScheme = keyboardScheme
        self.needTranslation = needTranslation
        
    def regenerate_inline_keyboard(self, languageName: str) -> InlineKeyboardMarkup:
        self.scheme = []
        
        if self.needTranslation:
            for buttons_row in self.__nameScheme:
                scheme_buttons_row = []
                
                for buttonDictionary in buttons_row:
                    buttonName = list(buttonDictionary.keys())[0]
                    button_text_translated = LANGUAGES[languageName]["BUTTONS"][buttonName]
                    scheme_buttons_row.append(InlineKeyboardButton(text=button_text_translated, **buttonDictionary[buttonName]))
                    
                self.scheme.append(scheme_buttons_row)
        else:
            self.scheme = self.__nameScheme.copy()
            
        return InlineKeyboardMarkup(inline_keyboard=self.scheme)
    
    def regenerate_reply_keyboard(self, languageName: str) -> ReplyKeyboardMarkup:
        self.scheme = []
        
        if self.needTranslation:
            for buttons_row in self.__nameScheme:
                scheme_buttons_row = []
                
                for buttonDictionary in buttons_row:
                    buttonName = list(buttonDictionary.keys())[0]
                    button_text_translated = LANGUAGES[languageName]["BUTTONS"][buttonName]
                    scheme_buttons_row.append(KeyboardButton(text=button_text_translated, **buttonDictionary[buttonName]))
                    
                self.scheme.append(scheme_buttons_row)
        else:
            self.scheme = self.__nameScheme.copy()
            
        return ReplyKeyboardMarkup(keyboard=self.scheme, resize_keyboard=True)
            
class KeyboardController(metaclass=Singleton):    
    def __init__(self):
        self.keyboards = {}
        
    def add_keyboard(self, keyboardName: str, keyboard: Keyboard):
        self.keyboards[keyboardName] = keyboard
        
    def get_keyboard(self, keyboardName: str, keyboardType: int, languageName: str) -> Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]:
        return self.keyboards[keyboardName].regenerate_reply_keyboard(languageName=languageName) if keyboardType == KeyboardType.REPLY else self.keyboards[keyboardName].regenerate_inline_keyboard(languageName=languageName)
        
    
        
