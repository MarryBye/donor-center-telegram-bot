from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import Union

from src.funcs.core import get_language_phrases

class Keyboard:
    def __init__(self, scheme: list):
        self.name_scheme = scheme
        self.scheme = None
        
        self.load_for(id=-1)
        
    def create_keyboard(self):
        self.keyboard = ReplyKeyboardMarkup(keyboard=self.scheme, resize_keyboard=True)

    def load_for(self, id: Union[int, str]):
        for i, buttons_row in enumerate(self.name_scheme):
            scheme_buttons_row = []
            for i, button in enumerate(buttons_row):
                scheme_buttons_row[i] = KeyboardButton(text=get_language_phrases(id=id)["BUTTONS"][button])
            self.scheme[i] = scheme_buttons_row
        self.create_keyboard()
            

        