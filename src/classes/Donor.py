from src.classes.CRMBaseDataType import CRMBaseDataType


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

    def set_gender(self, gender_id: int):
        self.data["gender_ID"] = gender_id

    def get_gender(self) -> int:
        return self.get_from_data(key_name="gender_ID")

    def set_email(self, email: str):
        self.data["email"] = email

    def get_email(self) -> str:
        return self.get_from_data(key_name="email")

    def set_telegram(self, telegram_id: int):
        self.data["telegram_ID"] = telegram_id

    def get_telegram(self) -> int:
        return self.get_from_data(key_name="telegram_ID")

    def set_password(self, password: str):
        self.data["password"] = password

    def get_password(self) -> str:
        return self.get_from_data(key_name="password")

    def set_language(self, language_id: int):
        self.data["language_ID"] = language_id

    def get_language(self) -> int:
        return self.get_from_data(key_name="language_ID")

    def set_number_id(self, number_id: int):
        self.data["number_ID"] = number_id

    def get_number_id(self) -> int:
        return self.get_from_data(key_name="number_ID")

    def set_number(self, number: str):
        self.data["number"] = number

    def get_number(self) -> str:
        return self.get_from_data(key_name="number")
