from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.CRMBot import CRMBot
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, KeyboardName, KeyboardType
from src.funcs.debug_print import debug_print

bot = CRMBot()

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()

router = Router(name="User commands router")


@router.message(Command("cancel"))
async def main_handler(msg: Message, state: FSMContext):

    user_id = msg.from_user.id
    user_language = db.get_user_language(user_id=user_id)

    if await state.get_state() is not None:
        await state.clear()

    await bot.answer(
        user_id=user_id,
        text="CANCELLED_STATE",
        keyboard_name=KeyboardName.MAIN,
        keyboard_type=KeyboardType.REPLY,
        language_name=user_language,
    )

    debug_print("User", user_id, "has cancelled last command!")


hnd.add_router(router)
