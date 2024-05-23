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

a = DatabaseController().get_clinic(clinic_id=1).get_address().get_city().get_city_name()

print(a)
