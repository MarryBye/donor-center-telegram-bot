from src.classes.Datatypes.CRMBaseDataType import CRMBaseDataType
from src.classes.Datatypes.Gender import Gender
from src.classes.Datatypes.Language import Language
from src.classes.Datatypes.Telephone import Telephone


class Donor(CRMBaseDataType):
    """

    Формирует объект донора при помощи данных из БД. Метод ``form()`` для формирования нового донора. В качестве
    аргумента нужно передать кортеж данных из БД. Например ``new_donor.form(data)``, где ``data`` - это кортеж.

    """

    def set_name(self, name: str):
        self.data["name_donor"] = name

    def get_name(self) -> str:
        return self.get_from_data(key_name="name_donor")

    def set_surname(self, surname: str):
        self.data["surname_donor"] = surname

    def get_surname(self) -> str:
        return self.get_from_data(key_name="surname_donor")

    def set_birthdate(self, birthdate: str):
        self.data["date_of_birth"] = birthdate

    def get_birthdate(self) -> str:
        return self.get_from_data(key_name="date_of_birth")

    def set_gender(self, gender: Gender):
        self.data["gender"] = gender

    def get_gender(self) -> Gender:
        return self.get_from_data(key_name="gender")

    def set_email(self, email: str):
        self.data["email"] = email

    def get_email(self) -> str:
        return self.get_from_data(key_name="email")

    def set_telegram_id(self, telegram_id: int):
        self.data["telegram_ID"] = telegram_id

    def get_telegram_id(self) -> int:
        return self.get_from_data(key_name="telegram_ID")

    def set_password(self, password: str):
        self.data["password"] = password

    def get_password(self) -> str:
        return self.get_from_data(key_name="password")

    def set_language(self, language: Language):
        self.data["language"] = language

    def get_language(self) -> Language:
        return self.get_from_data(key_name="language")

    def set_telephone(self, telephone: Telephone):
        self.data["telephone"] = telephone

    def get_telephone(self) -> Telephone:
        return self.get_from_data(key_name="telephone")
