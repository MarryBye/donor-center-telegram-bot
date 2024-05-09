from src.classes.CRMBaseDataType import CRMBaseDataType

class Donor(CRMBaseDataType):
    
    '''
    Формирует объект донора при помощи данных из БД. Метод ``form()`` для формирования нового донора. В качестве аргумента нужно передать кортеж данных из БД. Например ``new_donor.form(data)``, где ``data`` - это кортеж.
    '''
    
    def set_name(self, name: str):
        self.data["name_donor"] = name
    
    def get_name(self) -> str:
        return self.data["name_donor"]
    
    def set_surname(self, surname: str):
        self.data["surname_donor"] = surname
    
    def get_surname(self) -> str:
        return self.data["surname_donor"]
    
    def set_birthdate(self, birthdate: str):
        self.data["date_of_birth"] = birthdate
    
    def get_birthdate(self) -> str:
        return self.data["date_of_birth"]
    
    def set_gender(self, gender: int):
        self.data["gender_ID"] = gender
    
    def get_gender(self) -> int:
        return self.data["gender_ID"]
    
    def set_email(self, email: str):
        self.data["email"] = email
    
    def get_email(self) -> str:
        return self.data["email"]
    
    def set_telegram(self, telegram: int):
        self.data["telegram_ID"] = telegram
    
    def get_telegram(self) -> int:
        return self.data["telegram_ID"]
    
    def set_password(self, password: str):
        self.data["password"] = password
    
    def get_password(self) -> str:
        return self.data["password"]
    
    def set_language(self, language: int):
        self.data["language_ID"] = language
    
    def get_language(self) -> int:
        return self.data["language_ID"]
    
    def set_number_id(self, id: int):
        self.data["number_ID"] = id
    
    def get_number_id(self) -> int:
        return self.data["number_ID"]
    
    def set_number(self, number: str):
        self.data["donor_number"] = number
    
    def get_number(self) -> int:
        return self.data["donor_number"]
    