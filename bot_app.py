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

# new_donor = Donor()

# new_donor.set_name(name="Abobius")
# new_donor.set_surname(surname="Aborimbas")
# new_donor.set_birthdate(birthdate="12-12-2000")
# new_donor.set_gender(gender=1)
# new_donor.set_telegram(telegram=222122221112)
# new_donor.set_language(language=3)
# new_donor.set_email(email="a343512221111@gmail.com")
# new_donor.set_number(number="+22233334324")
# new_donor.set_password(password="hui")

# print(DatabaseController().register_donor(donor=new_donor))

# for donor in DatabaseController().get_donors():
#     print(donor.get_name(), Crypto().decode(donor.get_password()))

# new_appointment = Appointment()
# new_appointment.set_registration_date("12-12-2025")
# new_appointment.set_clinic_id(clinic_ID=2)
# new_appointment.set_appointment_date("11-11-2026")
# new_appointment.set_analysis_file_path("log.txt")
# new_appointment.set_donor_number_ID(donor_number_ID=7)

# print(DatabaseController().register_donor(donor=new_donor))
# print(DatabaseController().is_registered_donor_appointment(donor=DatabaseController().get_donor_by(id=8)))
# print(DatabaseController().register_donor_appointment(donor=DatabaseController().get_donor_by(id=8), appointment=Appointment()))

# print(DatabaseController().get_donor_by(id=1).get_name())
# print(DatabaseController().delete_donor(donor=DatabaseController().get_donor_by(id=1)))
# print(DatabaseController().get_donor_by(id=1).get_name())