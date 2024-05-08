class Donor:
    
    '''
    Формирует объект донора при помощи данных из БД. Метод ``form()`` для формирования нового донора. В качестве аргумента нужно передать кортеж данных из БД. Например ``new_donor.form(data)``, где ``data`` - это кортеж.
    '''
    
    def __init__(self, data: tuple=None):
        self.__data = {
            "ID": None,
            "name_donor": None,
            "surname_donor": None,
            "date_of_birth": None,
            "gender_ID": None,
            "email": None,
            "telegram_ID": None,
            "password": None,
            "language_ID": None,
            "number_ID": None,
            "donor_number": None
        }
        
        if data is not None:
            self.form(data)
        
    def form(self, data: tuple):
        for i, data_component in enumerate(self.__data, start=0):
            self.__data[data_component] = data[i]
            
        return self
    
    def get_data(self) -> tuple:
        return self.__data.values()
    
    def set_id(self, id: int):
        self.__data["ID"] = id
    
    def get_id(self) -> int:
        return self.__data["ID"]
    
    def set_name(self, name: str):
        self.__data["name_donor"] = name
    
    def get_name(self) -> str:
        return self.__data["name_donor"]
    
    def set_surname(self, surname: str):
        self.__data["surname_donor"] = surname
    
    def get_surname(self) -> str:
        return self.__data["surname_donor"]
    
    def set_birthdate(self, birthdate: str):
        self.__data["date_of_birth"] = birthdate
    
    def get_birthdate(self) -> str:
        return self.__data["date_of_birth"]
    
    def set_gender(self, gender: int):
        self.__data["gender_ID"] = gender
    
    def get_gender(self) -> int:
        return self.__data["gender_ID"]
    
    def set_email(self, email: str):
        self.__data["email"] = email
    
    def get_email(self) -> str:
        return self.__data["email"]
    
    def set_telegram(self, telegram: int):
        self.__data["telegram_ID"] = telegram
    
    def get_telegram(self) -> int:
        return self.__data["telegram_ID"]
    
    def set_password(self, password: str):
        self.__data["password"] = password
    
    def get_password(self) -> str:
        return self.__data["password"]
    
    def set_language(self, language: int):
        self.__data["language_ID"] = language
    
    def get_language(self) -> int:
        return self.__data["language_ID"]
    
    def set_number_id(self, id: int):
        self.__data["number_ID"] = id
    
    def get_number_id(self) -> int:
        return self.__data["number_ID"]
    
    def set_number(self, number: str):
        self.__data["donor_number"] = number
    
    def get_number(self) -> int:
        return self.__data["donor_number"]
    