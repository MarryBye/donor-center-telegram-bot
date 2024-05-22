import config as cfg

from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardRemove

from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Keyboards import KeyboardController, Keyboard, KeyboardName, KeyboardType
from src.classes.Singleton import Singleton

from src.funcs.core import message_translate
from src.funcs.debug_print import debug_print

db = DatabaseController()
hnd = HandlersController()
kb = KeyboardController()


class CRMBot(Bot, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(token=cfg.TOKEN, *args, **kwargs)

        self.dispatcher = Dispatcher()

        debug_print("CRMBot class has been initialized!")

    def include_routers(self):
        debug_print("Loading of routers has started!")
        for rt in hnd.get_routers():
            debug_print(rt.name, " has successfully connected!")
            self.dispatcher.include_router(rt)

    async def send_notifications(self, message: str):
        for user in db.get_notifications_list():
            debug_print("Sending notification to", user)
            await self.send_message(user, message)

    async def start_bot(self):
        await self.delete_webhook(drop_pending_updates=True)
        bot_name = await self.get_my_name()
        debug_print(bot_name.name, "is alive and ready to work!")
        await self.dispatcher.start_polling(self)

    async def answer(self, user_id: int, text: str, need_translation: bool = True, keyboard_name: KeyboardName | str | Keyboard = None, keyboard_type: KeyboardType | int = None, language_name: str = cfg.DEFAULT_LANGUAGE):

        if type(keyboard_name) is not Keyboard:
            new_keyboard = kb.get_keyboard(
                keyboard_name=keyboard_name,
                keyboard_type=keyboard_type,
                language_name=language_name
            ) if keyboard_name is not None else ReplyKeyboardRemove()
        else:
            if keyboard_type is KeyboardType.REPLY:
                new_keyboard = keyboard_name.regenerate_reply_keyboard(language_name=language_name)
            else:
                new_keyboard = keyboard_name.regenerate_inline_keyboard(language_name=language_name)

        bot_message = message_translate(
            message_name=text,
            language_name=language_name
        ) if need_translation else text

        debug_print("Sending answer to", user_id)

        return await self.send_message(user_id, text=bot_message, reply_markup=new_keyboard)
