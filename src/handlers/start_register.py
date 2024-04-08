import asyncio
import config as cfg

from re import match
from random import choice

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.classes.CRMBot import CRMBot
from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.classes.Form import Form, Feedback

from src.funcs.core import pressed_button, message_translate, button_translate, language_name_to_id, gender_name_to_id, get_command_variations

bot = CRMBot()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="REGISTER ROUTER")

@router.message(Command("start"))
async def main_handler(msg: Message, state: FSMContext):
    
    user_id = msg.from_user.id
    
    if not db.get_donor_by_userid(user_id=user_id):
    
        await state.set_state(Form.registerUser_contact)
        
        db.set_user_notifications(user_id=user_id, option=True)
        db.set_user_language(user_id=msg.from_user.id, language=cfg.DEFAULT_LANGUAGE)
        
        new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.MSG_SHARECONTACT, keyboardType=KeyboardType.REPLY, languageName=cfg.DEFAULT_LANGUAGE)
        bot_message = message_translate(message_name="REGISTER_START", language_name=cfg.DEFAULT_LANGUAGE)
                
        await msg.reply(text=bot_message, reply_markup=new_keyboard)
        
    else:
        
        new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.MAIN, keyboardType=KeyboardType.REPLY, languageName=cfg.DEFAULT_LANGUAGE)
        bot_message = message_translate(message_name="ALREADY_REGISTERED", language_name=cfg.DEFAULT_LANGUAGE)
                
        await msg.reply(text=bot_message, reply_markup=new_keyboard)
        

@router.message(Form.registerUser_contact)
async def main_handler(msg: Message, state: FSMContext):
    
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    user_contact = msg.contact
    
    if user_contact is not None:
        
        user_phone = user_contact.phone_number
        user_firstname = user_contact.first_name
        user_lastname = user_contact.last_name
        
        await state.update_data(user_phone=user_phone)
        await state.update_data(user_firstname=user_firstname)
        await state.update_data(user_lastname=user_lastname)
        
        await state.set_state(Form.registerUser_birthday)
        
        bot_message = message_translate(message_name="REGISTER_STEP_1", language_name=user_language)
            
        await msg.reply(text=bot_message, reply_markup=None)
        
    else:
        new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.MSG_SHARECONTACT, keyboardType=KeyboardType.REPLY, languageName=cfg.DEFAULT_LANGUAGE)
        bot_message = message_translate(message_name="REGISTER_START_FAILURE", language_name=user_language)
            
        await msg.reply(text=bot_message, reply_markup=new_keyboard)
        
@router.message(Form.registerUser_birthday)
async def main_handler(msg: Message, state: FSMContext):
    
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    
    birthday_pattern = r'^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(19[4-9][0-9]|20[0-9]{2})$'
    
    if msg.text is None or not match(birthday_pattern, msg.text):
        bot_message = message_translate(message_name="REGISTER_STEP_1_FAILURE", language_name=user_language)
            
        await msg.reply(text=bot_message, reply_markup=None)
    
    elif match(birthday_pattern, msg.text):
        user_birthday = msg.text
        
        await state.update_data(user_birthday=user_birthday)
    
        await state.set_state(Form.registerUser_gender)
        
        new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.GENDERS, keyboardType=KeyboardType.REPLY, languageName=user_language)
        bot_message = message_translate(message_name="REGISTER_STEP_2", language_name=user_language)
            
        await msg.reply(text=bot_message, reply_markup=new_keyboard)

@router.message(Form.registerUser_gender)
async def main_handler(msg: Message, state: FSMContext):
    
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    
    if msg.text in get_command_variations(button_name="MALE") or msg.text in get_command_variations(button_name="FEMALE") or msg.text in get_command_variations(button_name="OTHER") or msg.text in get_command_variations(button_name="NODATA"):
        
        user_gender = ""
        
        if msg.text in get_command_variations(button_name="MALE"):
            user_gender = "MALE"
    
        if msg.text in msg.text in get_command_variations(button_name="FEMALE"):
            user_gender = "FEMALE"
    
        if msg.text in get_command_variations(button_name="OTHER"):
            user_gender = "OTHER"
    
        if msg.text in get_command_variations(button_name="NODATA"):
            user_gender = "NODATA"
        
        await state.update_data(user_gender=user_gender)
        
        await state.set_state(Form.registerUser_password)
        
        bot_message = message_translate(message_name="REGISTER_STEP_3", language_name=user_language)
        
        await msg.reply(text=bot_message, reply_markup=None)
    else:
        new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.GENDERS, keyboardType=KeyboardType.REPLY, languageName=user_language)
        bot_message = message_translate(message_name="REGISTER_STEP_2_FAILURE", language_name=user_language)
            
        await msg.reply(text=bot_message, reply_markup=new_keyboard)
        
@router.message(Form.registerUser_password)
async def main_handler(msg: Message, state: FSMContext):
    
    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)
    
    passwod_pattern = r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z0-9]{8,}$'
    
    if msg.text is None or not match(passwod_pattern, msg.text):
        bot_message = message_translate(message_name="REGISTER_STEP_3_FAILURE", language_name=user_language)
            
        await msg.reply(text=bot_message, reply_markup=None)
        
    elif match(passwod_pattern, msg.text):
        user_password = msg.text
        
        await state.update_data(user_password=user_password)
        
        user_data = await state.get_data()
        
        user_firstname = user_data["user_firstname"]
        user_lastname = user_data["user_lastname"]
        user_birthday = user_data["user_birthday"]
        user_gender = user_data["user_gender"]
        user_password = user_data["user_password"]
        user_phone = user_data["user_phone"]
        
        user_language_id = language_name_to_id(language_name=user_language)
        user_gender_id = gender_name_to_id(gender_name=user_gender)
        
        db.set_user_phone(user_id=user_id, user_phone=user_phone)
        db.register_donor(name=user_firstname, surname=user_lastname, date_of_birth=user_birthday, password=user_password, gender_id=user_gender_id, language=user_language_id, user_phone=user_phone)
        
        new_keyboard = kb.get_keyboard(keyboardName=KeyboardName.MAIN, keyboardType=KeyboardType.REPLY, languageName=cfg.DEFAULT_LANGUAGE)
        bot_message = message_translate(message_name="SUCCESSFULL_REGISTER", language_name=user_language)
        
        await state.clear()
            
        await msg.reply(text=bot_message, reply_markup=new_keyboard)
        
hnd.add_router(router)