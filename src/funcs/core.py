from aiogram import F

import config as cfg
from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.Keyboards import KeyboardButton, ReplyKeyboardMarkup
from src.lang.languages import LANGUAGES

db = DatabaseController()


# Language translations for buttons and messages


def get_command_variations(button_name: str):
    """Возвращает кортеж с возможными написаниями команды на разных языках, предусмотренных в боте"""
    command_variations = []
    for language in LANGUAGES:
        command_variations.append(LANGUAGES[language]["BUTTONS"][button_name])
    return command_variations


def pressed_button(button_name: str):
    """Сокращенный магический фильтр, проверяет была ли нажата кнопка по ее названию, проверяя все ее переводы"""
    return F.text.in_(get_command_variations(button_name=button_name))


def sent_callback(callback_name: str):
    """Сокращенный магический фильтр, проверяет совпадение значения от Inline кнопки"""
    return F.data == callback_name


def message_translate(message_name: str, language_name: str):
    """Возвращает текст сообщения, переведенный на указанный язык"""
    return LANGUAGES[language_name]["MESSAGES"][message_name]


def button_translate(button_name: str, language_name: str):
    """Возвращает текст кнопки, переведенный на указанный язык"""
    return LANGUAGES[language_name]["BUTTONS"][button_name]


# Data tranformation


def month_name_to_id(month_name: str):
    for i in range(12):
        if month_name in get_command_variations("REGISTER_MONTH_" + str(i + 1)):
            return i + 1


def language_name_to_id(language_name: str):
    for language in cfg.LANGUAGES:
        if language_name in language:
            return language[0]


def blood_name_to_id(blood_name: str):
    for blood in cfg.BLOODS:
        if blood_name == blood[1] + blood[2]:
            return blood[0]


def gender_name_to_id(gender_name: str):
    for gender in cfg.GENDERS:
        if gender[1] == gender_name:
            return gender[0]


def generate_keyboard_days(month: int, year: int):
    months_days = {
        1: 31,
        2: 29 if year % 4 == 0 else 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }

    days_count = months_days[month]
    i = 0

    kb_scheme = []

    row = []

    while days_count - i > 0:
        row.append(KeyboardButton(text=str(days_count - i)))
        i += 1

        if len(row) == 5 or days_count - i == 0:
            kb_scheme.append(row)
            row = []

    return ReplyKeyboardMarkup(keyboard=kb_scheme, resize_keyboard=True)


def generate_keyboard_bloods():
    kb_scheme = []

    for blood in cfg.BLOODS:
        kb_scheme.append([KeyboardButton(text=blood[1] + blood[2])])

    return ReplyKeyboardMarkup(keyboard=kb_scheme, resize_keyboard=True)
