# from handlers_imports import *
# from keyboards_imports import *

from src.classes.DatabaseControllers.DatabaseController import DatabaseController
from src.classes.DatabaseControllers.DonorsDatabaseController import DonorsDatabaseController
from src.classes.DatabaseControllers.AppointmentsDatabaseController import AppointmentsDatabaseController

# id_my = 482613937

# bot = CRMBot()
#
# bot.include_routers()
#
# if __name__ == "__main__":
#     #DatabaseController().setup_database()
#     asyncio.run(bot.start_bot())

d = DatabaseController().get_donor(telegram_id=482613937)
a = DatabaseController().get_donor_appointments(donor=d).get_donor().get_email()

print(a)
