import config as cfg

from datetime import date

from typing import Union
from aiogram import F

from src.classes.DatabaseController import DatabaseController
from src.classes.Keyboards import Keyboard, ReplyKeyboardMarkup, KeyboardButton

from src.lang.languages import LANGUAGES

db = DatabaseController()

# Language translations for buttons and messages

def get_command_variations(key: str):
    command_variations = []
    for language in LANGUAGES:
        command_variations.append(LANGUAGES[language]["BUTTONS"][key])
    return command_variations

def is_pressed_kb_button(key: str):
    return F.text.in_(get_command_variations(key=key))

def is_sended_callback(key: str):
    return F.data == key

def message_translated(user_id: Union[int, str], key: str):
    return LANGUAGES[db.get_user_language(user_id=user_id)]["MESSAGES"][key]

def button_translated(user_id: Union[int, str], key: str):
    return LANGUAGES[db.get_user_language(user_id=user_id)]["BUTTONS"][key]

# Data tranformation

def month_name_to_number(month: str):
    for i in range(12):
        if month in get_command_variations("REGISTER_MONTH_" + str(i + 1)):
            return i + 1
        
def language_name_to_number(language: str):
    for language_tuple in cfg.LANGUAGES:
        if language in language_tuple:
            return language_tuple[0]

def blood_name_to_number(blood: str):
    for blood_tuple in cfg.BLOODS:
        if blood == blood_tuple[1] + blood_tuple[2]:
            return blood_tuple[0]
        
def gender_name_to_number(gender: str):
    # немного костыльно, можно сравнивать конец названия кнопки но помоему это еще хуже
    
    if gender in get_command_variations("REGISTER_GENDER_MALE"):
        gender = "Male"
    if gender in get_command_variations("REGISTER_GENDER_FEMALE"):
        gender = "Female"
    if gender in get_command_variations("REGISTER_GENDER_OTHER"):
        gender = "Other"
    if gender in get_command_variations("REGISTER_GENDER_SECRET"):
        gender = "Secret"
        
    for gender_tuple in cfg.GENDERS:
        if gender in gender_tuple:
            return gender_tuple[0]

# Keyboards generation

def generate_keyboard_months():
    kb_scheme = [
        ["REGISTER_MONTH_1", "REGISTER_MONTH_2", "REGISTER_MONTH_3"],
        ["REGISTER_MONTH_4", "REGISTER_MONTH_5", "REGISTER_MONTH_6"],
        ["REGISTER_MONTH_7", "REGISTER_MONTH_8", "REGISTER_MONTH_9"],
        ["REGISTER_MONTH_10", "REGISTER_MONTH_11", "REGISTER_MONTH_12"]
    ]

    return Keyboard(keyboard=kb_scheme)

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
        12: 31
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

def generate_keyboard_years():
    current_year = date.today().year
    minimum_year = current_year - cfg.DONATION_MAXIMUM_YEAR
    
    kb_scheme = []
    
    row = []
    for year in range(current_year, minimum_year + 1, -1):
        if len(row) < 5:
            row.append(KeyboardButton(text=str(year)))
        else:
            kb_scheme.append(row)
            row = []
    
    return ReplyKeyboardMarkup(keyboard=kb_scheme, resize_keyboard=True)

def generate_keyboard_bloods():
    
    kb_scheme = []
    
    for blood in cfg.BLOODS:
        kb_scheme.append([KeyboardButton(text=blood[1] + blood[2])])
        
    return ReplyKeyboardMarkup(keyboard=kb_scheme, resize_keyboard=True)

def generate_keyboard_genders():
    
    kb_scheme = [
        ["REGISTER_GENDER_MALE", "REGISTER_GENDER_FEMALE"],
        ["REGISTER_GENDER_OTHER"],
        ["REGISTER_GENDER_SECRET"]
    ]
        
    return Keyboard(keyboard=kb_scheme)