import asyncio
import config as cfg

from aiogram import Bot, Dispatcher

from src.classes.HandlersController import HandlersController

from handlers_imports import *
from keyboards_imports import *

from src.lang.languages import LANGUAGES

# id_my = 482613937

async def main():
    
    bot = Bot(token=cfg.TOKEN)
    
    dispatcher = Dispatcher()
    
    for rt in HandlersController().get_routers():
        dispatcher.include_router(rt)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())