import asyncio
import config as cfg

from src.classes.CRMBot import CRMBot
from src.classes.DatabaseController import DatabaseController
from src.classes.Donor import *

from handlers_imports import *
from keyboards_imports import *

# id_my = 482613937

# bot = CRMBot()

# bot.include_routers()

# if __name__ == "__main__":
#     #DatabaseController().setup_database()
#     asyncio.run(bot.start_bot())

# new_donor = Donor().form((145, "Bob", "Atkins", "18.09.2004", 1, "bob@gmail.com", 1667488673, "2E4f555U", 2, 1))

for donor in DatabaseController().get_donors():
    print(donor.get_name())