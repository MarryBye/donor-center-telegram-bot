from src.classes.CRMBaseDataType import CRMBaseDataType

class Appointment(CRMBaseDataType):
    
    '''
    Формирует объект записи на прием при помощи данных из БД. Метод ``form()`` для формирования новой записи. В качестве аргумента нужно передать кортеж данных из БД. Например ``new_appointment.form(data)``, где ``data`` - это кортеж.
    '''
    
    def set_clinic_id(self, clinic_ID: int):
        self.data["clinic_ID"] = clinic_ID
        
    def get_clinic_id(self) -> int:
        return self.data["clinic_ID"]
    
    def set_donor_number_ID(self, donor_number_ID):
        self.data["donor_number_ID"] = donor_number_ID
        
    def get_donor_number_ID(self) -> int:
        return self.data["donor_number_ID"]
    
    def set_status_ID(self, status_ID):
        self.data["status_ID"] = status_ID
        
    def get_status_ID(self) -> int:
        return self.data["status_ID"]
    
    def set_registration_date(self, registration_date: str):
        self.data["registration_date"] = registration_date
        
    def get_registration_date(self) -> str:
        return self.data["registration_date"]
    
    def set_appointment_date(self, appointment_date: str):
        self.data["appointment_date"] = appointment_date
        
    def get_appointment_date(self) -> str:
        return self.data["appointment_date"]
    
    def set_analysis_file_path(self, analysis_file_path: str):
        self.data["analysis_file_path"] = analysis_file_path
        
    def get_analysis_file_path(self) -> str:
        return self.data["analysis_file_path"]