import asyncio
import config as cfg

from src.classes.CRMBot import CRMBot

from handlers_imports import *
from keyboards_imports import *

# id_my = 482613937

bot = CRMBot()

bot.include_routers()

if __name__ == "__main__":
    asyncio.run(bot.start_bot())