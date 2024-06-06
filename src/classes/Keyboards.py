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
    GENDERS = "GENDERS"
    LANGUAGES_REGISTER = "LANGUAGES_REGISTER"
    CITIES = "CITIES"
    REGIONS = "REGIONS"
    EDIT_PROFILE = "EDIT_PROFILE"
    PROFILE_SETTINGS = "PROFILE_SETTINGS"
    ADMIN = "ADMIN"
    STATISTIC = "STATISTIC"
    STATUSES = "STATUSES"


class Keyboard:
    def __init__(self, keyboard_scheme: list[list[dict[str, dict]]], need_translation=True):
        self.scheme = None
        self.__nameScheme = keyboard_scheme
        self.need_translation = need_translation

    def regenerate_inline_keyboard(self, language_name: str) -> InlineKeyboardMarkup:
        self.scheme = []

        for buttons_row in self.__nameScheme:
            scheme_buttons_row = []

            for button_dictionary in buttons_row:
                button_name = list(button_dictionary.keys())[0]
                if self.need_translation:
                    button_text = LANGUAGES[language_name]["BUTTONS"][button_name]
                else:
                    button_text = button_name
                scheme_buttons_row.append(InlineKeyboardButton(text=button_text, **button_dictionary[button_name]))

            self.scheme.append(scheme_buttons_row)

        return InlineKeyboardMarkup(inline_keyboard=self.scheme)

    def regenerate_reply_keyboard(self, language_name: str) -> ReplyKeyboardMarkup:
        self.scheme = []

        for buttons_row in self.__nameScheme:
            scheme_buttons_row = []

            for button_dictionary in buttons_row:
                button_name = list(button_dictionary.keys())[0]
                if self.need_translation:
                    button_text = LANGUAGES[language_name]["BUTTONS"][button_name]
                else:
                    button_text = button_name
                scheme_buttons_row.append(
                    KeyboardButton(text=button_text, **button_dictionary[button_name]))

            self.scheme.append(scheme_buttons_row)

        return ReplyKeyboardMarkup(keyboard=self.scheme, resize_keyboard=True)


class KeyboardController(metaclass=Singleton):
    def __init__(self):
        self.keyboards = {}

    def add_keyboard(self, keyboard_name: KeyboardName | str, keyboard: Keyboard):
        self.keyboards[keyboard_name] = keyboard

    def get_keyboard(self, keyboard_name: KeyboardName | str, keyboard_type: KeyboardType | int, language_name: str) -> Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]:
        return self.keyboards[keyboard_name].regenerate_reply_keyboard(
            language_name=language_name) if keyboard_type == KeyboardType.REPLY else self.keyboards[
            keyboard_name].regenerate_inline_keyboard(language_name=language_name)
