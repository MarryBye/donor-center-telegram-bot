from handlers_imports import *
from keyboards_imports import *

from src.classes.Controllers.DatabaseController import DatabaseController

# id_my = 482613937

bot = CRMBot()

bot.include_routers()

if __name__ == "__main__":
    #DatabaseController().setup_database()
    asyncio.run(bot.start_bot())