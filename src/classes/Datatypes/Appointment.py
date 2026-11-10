from src.classes.Datatypes.Clinic import Clinic
from src.classes.Datatypes.CRMBaseDataType import CRMBaseDataType
from src.classes.Datatypes.Donor import Donor
from src.classes.Datatypes.Status import Status


class Appointment(CRMBaseDataType):
    """
    Формирует объект записи на прием при помощи данных из БД. Метод ``form()`` для формирования новой записи. В
    качестве аргумента нужно передать кортеж данных из БД. Например ``new_appointment.form(data)``, где ``data`` -
    это кортеж.
    """

    def set_clinic(self, clinic: Clinic):
        self.data["clinic"] = clinic

    def get_clinic(self) -> Clinic:
        return self.get_from_data(key_name="clinic")

    def set_donor(self, donor: Donor):
        self.data["donor"] = donor

    def get_donor(self) -> Donor:
        return self.get_from_data(key_name="donor")

    def set_status(self, status: Status):
        self.data["status"] = status

    def get_status(self) -> Status:
        return self.get_from_data(key_name="status")

    def set_registration_date(self, registration_date: str):
        self.data["registration_date"] = registration_date

    def get_registration_date(self) -> str:
        return self.get_from_data(key_name="registration_date")

    def set_appointment_date(self, appointment_date: str):
        self.data["appointment_date"] = appointment_date

    def get_appointment_date(self) -> str:
        return self.get_from_data(key_name="appointment_date")

    def set_analysis_file_path(self, analysis_file_path: str):
        self.data["analysis_file_path"] = analysis_file_path

    def get_analysis_file_path(self) -> str:
        return self.get_from_data(key_name="analysis_file_path")
