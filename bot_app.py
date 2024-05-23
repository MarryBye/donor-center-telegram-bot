from src.classes.CRMBot import CRMBot
from src.classes.DatabaseController import DatabaseController

from handlers_imports import *
from keyboards_imports import *

# id_my = 482613937

bot = CRMBot()

bot.include_routers()

if __name__ == "__main__":
    #DatabaseController().setup_database()
    asyncio.run(bot.start_bot())
