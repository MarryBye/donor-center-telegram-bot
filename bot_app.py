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

new_donor = Donor()

new_donor.set_name(name="Abobius")
new_donor.set_surname(surname="Aborimbas")
new_donor.set_birthdate(birthdate="12-12-2000")
new_donor.set_gender(gender=1)
new_donor.set_telegram(telegram=2888774)
new_donor.set_language(language=1)
new_donor.set_email(email="abob111@gmail.com")
new_donor.set_number(number="+380660660666")
new_donor.set_password(password="2eRT3kGG")

print(DatabaseController().register_donor(donor=new_donor))

for donor in DatabaseController().get_donors():
    print(donor.get_name(), donor.get_telegram())