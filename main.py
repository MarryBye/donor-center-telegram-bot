import asyncio
import config as cfg

from aiogram import Bot, Dispatcher

from src.classes.HandlersController import HandlersController
from src.classes.KeyboardsController import KeyboardsController, KB
# from src.classes.DatabaseController import DatabaseController

# DatabaseController().setup_database()

from handlers_imports import *
from keyboards_imports import *

async def main():
    
    bot = Bot(token=cfg.TOKEN)
    
    dispatcher = Dispatcher()
    
    for rt in HandlersController().get_routers():
        dispatcher.include_router(rt)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())