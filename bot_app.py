import asyncio
import config as cfg

from src.classes.CRMBot import CRMBot
from src.classes.DatabaseController import DatabaseController
from src.classes.Donor import *
from src.classes.Appointment import Appointment
from src.classes.Crypto import Crypto

from handlers_imports import *
from keyboards_imports import *

# id_my = 482613937

bot = CRMBot()

bot.include_routers()

#DatabaseController().delete_donor(DatabaseController().get_donor_by(telegram_id=482613937))

if __name__ == "__main__":
    #DatabaseController().setup_database()
    asyncio.run(bot.start_bot())