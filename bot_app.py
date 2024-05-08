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
new_donor.set_telegram(telegram=288833774)
new_donor.set_language(language=1)
new_donor.set_email(email="a234231@gmail.com")
new_donor.set_number(number="+38066066220666")
new_donor.set_password(password="2eRT3kGG")

# print(DatabaseController().register_donor(donor=new_donor))

# for donor in DatabaseController().get_donors():
#     print(donor.get_name(), donor.get_telegram())

DatabaseController().register_donor_appointment(id=5, clinic_id=1, registration_date="1-1-2000", appointment_date="11-11-2004")