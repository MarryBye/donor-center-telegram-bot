from random import choice

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController
from src.classes.Form import Form

from src.funcs.core import is_pressed_kb_button, message_translated, button_translated, generate_keyboard_days, generate_keyboard_months, generate_keyboard_years, month_name_to_number, generate_keyboard_bloods, generate_keyboard_genders, blood_name_to_number, language_name_to_number, gender_name_to_number, date

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router()

@router.message(is_pressed_kb_button("DONATION_MENU_REGISTER"))
async def main_handler(msg: Message, state: FSMContext):
       
       user_id = msg.from_user.id
       
       if not db.get_donor(user_id=user_id):
              await state.set_state(Form.enter_name)
              
              bot_message = message_translated(user_id=user_id, key="REGISTER_STEP_1") % msg.from_user.username
                     
              await msg.reply(text=bot_message)
       else:
              new_keyboard = kb.get_keyboard(kb.DONATION).reload_for(user_id)
              bot_message = message_translated(user_id=user_id, key="CANNOT_REGISTER")
                     
              await msg.reply(text=bot_message, reply_markup=new_keyboard)
       
@router.message(Form.enter_name)
async def process_register(msg: Message, state: FSMContext):
       
       user_id = msg.from_user.id
       
       await state.update_data(name=msg.text)
       await state.set_state(Form.enter_gender)
       
       new_keyboard = generate_keyboard_genders().reload_for(user_id=user_id)
       bot_message = message_translated(user_id=user_id, key="REGISTER_STEP_2") % msg.from_user.username
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)
       
@router.message(Form.enter_gender)
async def process_register(msg: Message, state: FSMContext):
       
       user_id = msg.from_user.id
       
       await state.update_data(gender=msg.text)
       await state.set_state(Form.enter_birthYear)
       
       new_keyboard = generate_keyboard_years()
       bot_message = message_translated(user_id=user_id, key="REGISTER_STEP_3") % msg.from_user.username
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)
       
@router.message(Form.enter_birthYear)
async def process_register(msg: Message, state: FSMContext):
       
       user_id = msg.from_user.id
       
       await state.update_data(year=int(msg.text))
       await state.set_state(Form.enter_birthMonth)
       
       new_keyboard = generate_keyboard_months().reload_for(user_id=user_id)
       bot_message = message_translated(user_id=user_id, key="REGISTER_STEP_4") % msg.from_user.username
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)
       
@router.message(Form.enter_birthMonth)
async def process_register(msg: Message, state: FSMContext):
       
       user_id = msg.from_user.id
       
       await state.update_data(month=month_name_to_number(month=msg.text))
       await state.set_state(Form.enter_birthDay)
       
       data = await state.get_data()
       
       year, month = data["year"], data["month"]
       
       new_keyboard = generate_keyboard_days(month=month, year=year)
       bot_message = message_translated(user_id=user_id, key="REGISTER_STEP_5") % msg.from_user.username
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)
       
@router.message(Form.enter_birthDay)
async def process_register(msg: Message, state: FSMContext):
       
       user_id = msg.from_user.id
       
       await state.update_data(day=int(msg.text))
       await state.set_state(Form.enter_blood)
       
       new_keyboard = generate_keyboard_bloods()
       bot_message = message_translated(user_id=user_id, key="REGISTER_STEP_6") % msg.from_user.username
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)
       
@router.message(Form.enter_blood)
async def end_register(msg: Message, state: FSMContext):
       
       user_id = msg.from_user.id
       
       await state.update_data(blood=msg.text)
       full_data = await state.get_data()
       await state.clear()
       
       name = full_data["name"]
       gender = gender_name_to_number(full_data["gender"])
       blood = blood_name_to_number(full_data["blood"])
       language = language_name_to_number(db.get_user_language(user_id=user_id))
       day, month, year = full_data["day"], full_data["month"], full_data["year"]
       birthdate = f"{day}-{month}-{year}"
       
       db.register_donor(id=user_id, name=name, date=birthdate, gender=gender, language=language, blood=blood)
       
       new_keyboard = kb.get_keyboard(kb.MAIN).reload_for(user_id=user_id)
       bot_message = message_translated(user_id=user_id, key="SUCCESSFULL_REGISTER") % (msg.from_user.username, user_id, name, full_data["gender"], birthdate, date.today().year - year, full_data["blood"], db.get_user_language(user_id=user_id))
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)
       
@router.message(is_pressed_kb_button("DONATION_MENU_FIND_CENTER"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       
       new_keyboard = kb.get_keyboard(kb.DONATION).reload_for(user_id)
       bot_message = message_translated(user_id=user_id, key="DONATION_FIND_CENTERS_MESSAGE") % (msg.from_user.username, "абоба\nабоба\nабоба")
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)
       
@router.message(is_pressed_kb_button("DONATION_MENU_HISTORY"))
async def main_handler(msg: Message):
       
       user_id = msg.from_user.id
       
       new_keyboard = kb.get_keyboard(kb.DONATION).reload_for(user_id)
       bot_message = message_translated(user_id=user_id, key="DONATION_HISTORY_MESSAGE") % (msg.from_user.username, "7", "абоба\nабоба\nабоба")
              
       await msg.reply(text=bot_message, reply_markup=new_keyboard)

hnd.add_router(router)