import config as cfg

from typing import Union
from aiogram import Bot, Dispatcher

from src.classes.Singleton import Singleton
from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController

db = DatabaseController()
hnd = HandlersController()

class CRMBot(Bot, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(token=cfg.TOKEN, *args, **kwargs)
        
        self.dispatcher = Dispatcher()
        
    def include_routers(self):
        for rt in hnd.get_routers():
            self.dispatcher.include_router(rt)
    
    async def send_notifications(self, message: str):
        for user in db.get_user_notifications():
            await self.send_message(user, message)
        
    async def start_bot(self):
        await self.delete_webhook(drop_pending_updates=True)
        print(await self.get_my_name(), " уже работает!")
        await self.dispatcher.start_polling(self)