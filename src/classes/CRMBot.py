from aiogram import Bot, Dispatcher

import config as cfg
from src.classes.DatabaseController import DatabaseController
from src.classes.HandlersController import HandlersController
from src.classes.Singleton import Singleton

db = DatabaseController()
hnd = HandlersController()


class CRMBot(Bot, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(token=cfg.TOKEN, *args, **kwargs)

        self.dispatcher = Dispatcher()

    def include_routers(self):
        print("Подключаю роутеры...")
        for rt in hnd.get_routers():
            print(rt.name, "подключен!")
            self.dispatcher.include_router(rt)

    async def send_notifications(self, message: str):
        for user in db.get_notifications_list():
            await self.send_message(user, message)

    async def start_bot(self):
        await self.delete_webhook(drop_pending_updates=True)
        print(await self.get_my_name(), " уже работает!")
        await self.dispatcher.start_polling(self)
