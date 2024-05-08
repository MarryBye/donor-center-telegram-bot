import psycopg2 as psql
import config as cfg
import json

from typing import Union

from src.classes.Singleton import Singleton
from src.classes.Donor import Donor

class DatabaseController(metaclass=Singleton):
    def __init__(self):
        
        self.languages_cache = json.load(open("bot/cache/user_languages.json", "r", encoding="UTF-8"))
        self.notifications_cache = json.load(open("bot/cache/user_notifications.json", "r", encoding="UTF-8"))
        self.phones_cache = json.load(open("bot/cache/user_phones.json", "r", encoding="UTF-8"))
        
        self.__connection = None
        self.__cursor = None
        
        self.connect()
        
    def connect(self):
        self.__connection = psql.connect(database=cfg.DATABASE_NAME,
                        host=cfg.IP_ADDRESS,
                        user=cfg.USERNAME,
                        password=cfg.PASSWORD,
                        port=cfg.PORT)
        self.__cursor = self.__connection.cursor()
        
    def disconnect(self):
        self.__cursor.close()
        self.__connection.close()
    
    def add_bloods(self):
        
        query = 'DELETE FROM data_blood.blood_and_components'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO data_blood.blood_and_components ("ID", "blood_and_comp_name") VALUES (%s, %s)'
        self.__cursor.executemany(query, cfg.BLOODS)
        
        self.__connection.commit()
        
    def add_languages(self):
        
        query = 'DELETE FROM donor.language'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO donor.language ("ID", "lang_name") VALUES (%s, %s)'
        self.__cursor.executemany(query, cfg.LANGUAGES)
        
        self.__connection.commit()
        
    def add_cities(self):
        
        query = 'DELETE FROM data_blood.city'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO data_blood.city ("ID", "city_name") VALUES (%s, %s)'
        self.__cursor.executemany(query, cfg.CITIES)
        
        self.__connection.commit()
        
    def add_regions(self):
        
        query = 'DELETE FROM data_blood.region'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO data_blood.region ("ID", "region_name") VALUES (%s, %s)'
        self.__cursor.executemany(query, cfg.REGIONS)
        
        self.__connection.commit()
        
    def add_streets(self):
        
        query = 'DELETE FROM data_blood.street'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO data_blood.street ("ID", "street_name") VALUES (%s, %s)'
        self.__cursor.executemany(query, cfg.STREETS)
        
        self.__connection.commit()
        
    def add_areas(self):
        
        query = 'DELETE FROM data_blood.area'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO data_blood.area ("ID", "area_name") VALUES (%s, %s)'
        self.__cursor.executemany(query, cfg.AREAS)
        
        self.__connection.commit() 
        
    def add_addresses(self):
        
        query = 'DELETE FROM data_blood.address'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO data_blood.address ("ID", "region_ID", "city_ID", "area_ID", "street_ID", "house_number") VALUES (%s, %s, %s, %s, %s, %s)'
        self.__cursor.executemany(query, cfg.ADDRESSES)
        
        self.__connection.commit()
        
    def add_statuses(self):
        
        query = 'DELETE FROM data_blood.status_appointment'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO data_blood.status_appointment ("ID", "name_status") VALUES (%s, %s)'
        self.__cursor.executemany(query, cfg.STATUSES)
        
        self.__connection.commit()
        
    def add_genders(self):
        
        query = 'DELETE FROM donor.gender'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO donor.gender ("ID", "gender_name") VALUES (%s, %s)'
        self.__cursor.executemany(query, cfg.GENDERS)
        
        self.__connection.commit()
        
    def add_clinics(self):
        
        query = 'DELETE FROM data_blood.clinic'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO data_blood.clinic ("ID", "clinic_name", "address_ID", "working_hours") VALUES (%s, %s, %s, %s)'
        self.__cursor.executemany(query, cfg.CLINICS)
        
        self.__connection.commit()
    
    def get_next_row_id(self, table: str) -> int:
        
        '''
        Получение последнего доступного номера в таблице, указанной в аргументе ``table``.\n
        Метод возвращает число - следующая свободная строка в указанной таблице.
        '''
        
        query = 'SELECT "ID" FROM %s ORDER BY "ID" DESC' % table
        self.__cursor.execute(query)
        
        data = self.__cursor.fetchone()
        
        return 1 if data is None else data[0] + 1
    
    def is_donor_exists(self, id: int=-1, telegram_id: int=-1, number: str="-1", email: str="-1") -> bool:
        
        '''
        Проверка существует ли донор. В качестве параметров передается одно из или несколько следующих значений:
        - ``id`` - номер донора в БД; 
        - ``telegram_id`` - номер профиля Телеграма пользоваля;
        - ``number`` - номер телефона пользователя;
        - ``email`` - электронная почта пользователя.\n
        Возвращает ``False`` если донора не существует.
        '''
        
        query = 'SELECT donors."ID" FROM donor.donor AS donors, number_telephone.donor_number AS numbers WHERE donors."ID" = %s OR donors."telegram_ID" = %s OR numbers.number = %s OR donors.email = %s'
        self.__cursor.execute(query, (id, telegram_id, number, email))
        
        data = self.__cursor.fetchone()
        is_exists = data is not None
        
        return is_exists
        
    def get_donor_by(self, id: int=-1, telegram_id: int=-1, number: str="-1", email: str="-1") -> Union[Donor, bool]:
        
        '''
        Сформировать объект ``Donor`` по данным из БД, если донор существует. В качестве параметров передается одно из или несколько следующих значений:
        - ``id`` - номер донора в БД; 
        - ``telegram_id`` - номер профиля Телеграма пользоваля;
        - ``number`` - номер телефона пользователя;
        - ``email`` - электронная почта пользователя.\n
        Метод возвращает ``False`` если донора не существует.
        '''
        
        query = 'SELECT donors.*, numbers."ID" AS number_ID, numbers.number AS number FROM donor.donor as donors, number_telephone.donor_number AS numbers WHERE donors."ID" = numbers."donor_ID" AND (donors."ID" = %s OR donors."telegram_ID" = %s OR numbers.number = %s OR donors.email = %s)'
        self.__cursor.execute(query, (id, telegram_id, number, email))
        
        data = self.__cursor.fetchone()
        
        return Donor(data=data) if data is not None else False
    
    def get_donors(self) -> list[Donor]:
        
        '''
        Получить список всех доноров существующих в БД в виде объектов ``Donor``.
        '''
        
        query = 'SELECT donors.*, numbers."ID" AS number_ID, numbers.number AS number FROM donor.donor as donors, number_telephone.donor_number AS numbers WHERE donors."ID" = numbers."donor_ID"'
        self.__cursor.execute(query)
        
        data = self.__cursor.fetchall()

        for i, donor_data in enumerate(data, start=0):
            data[i] = Donor(data=donor_data)
        
        return data
    
    def register_donor(self, donor: Donor) -> bool:
        
        '''
        Регистрация донора и добавление его в БД. Если донор уже существует (такая электронная почта уже существует, номер телефона, номер в БД или номер профиля Телеграм) метод вернет ``False``, в случае успешного выполнения будет возвращено значение ``True``.
        '''
        
        is_exists = self.is_donor_exists(id=donor.get_id(), telegram_id=donor.get_telegram(), number=donor.get_number(), email=donor.get_email())
        
        if is_exists:
            return False
        
        donor.set_id(id=self.get_next_row_id(table="donor.donor"))
        donor.set_number_id(id=self.get_next_row_id(table="number_telephone.donor_number"))
        
        query = 'INSERT INTO donor.donor ("ID", "name_donor", "surname_donor", "date_of_birth", "gender_ID", "email", "telegram_ID", "password", "language_ID") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        self.__cursor.execute(query, (
            donor.get_id(), 
            donor.get_name(), 
            donor.get_surname(),
            donor.get_birthdate(), 
            donor.get_gender(), 
            donor.get_email(), 
            donor.get_telegram(), 
            donor.get_password(), 
            donor.get_language()
            )
        )
        
        query = 'INSERT INTO number_telephone.donor_number ("ID", "donor_ID", "number") VALUES (%s, %s, %s)'
        self.__cursor.execute(query, (
            donor.get_number_id(), 
            donor.get_id(), 
            donor.get_number()
            )
        ) 
        
        self.__connection.commit()
        
        return True
    
    def is_registered_donor_appointment(self, id: int=-1, telegram_id: int=-1, number: str="-1", email: str="-1"):
        
        '''
        Узнать, зарегистрирован ли донор на прием. В качестве параметров для определения донора передается одно из или несколько следующих значений:
        - ``id`` - номер донора в БД; 
        - ``telegram_id`` - номер профиля Телеграма пользоваля;
        - ``number`` - номер телефона пользователя;
        - ``email`` - электронная почта пользователя.\n
        Если донора не существует или нет записи на прием, метод возвращает ``False``. В других случаях он вернет ``True``.
        '''
        
        if not self.is_donor_exists(id=id, telegram_id=telegram_id, number=number, email=email):
            return None
        
        query = 'SELECT appointments.* FROM donor.donor AS donors, number_telephone.donor_number AS numbers, data_blood.appointment AS appointments WHERE appointments."status_ID" = 3 AND appointments."donor_number_ID" = numbers."ID" AND numbers."donor_ID" = donors."ID" AND (donors."ID" = %s OR donors."telegram_ID" = %s OR numbers.number = %s OR donors.email = %s)'
        self.__cursor.execute(query, (id, telegram_id, number, email))
        
        data = self.__cursor.fetchone()
        print(data)
        is_registered = data is not None
        
        return is_registered
    
    def register_donor_appointment(self, clinic_id: int, registration_date: str, appointment_date: str, id: int=-1, telegram_id: int=-1, number: str="-1", email: str="-1"):
        
        '''
        Зарегистрировать донора на прием. В качестве параметров для определения донора передается одно из или несколько следующих значений:
        - ``id`` - номер донора в БД; 
        - ``telegram_id`` - номер профиля Телеграма пользоваля;
        - ``number`` - номер телефона пользователя;
        - ``email`` - электронная почта пользователя.\n
        Достаточно передать один из аргументов для того, чтобы определить кого записать на прием.
        Далее необходимо передать аргументы для будущей записи на прием, а именно:
        - ``clinic_id`` - номер клиники;
        - ``registration_date`` - дата регистрации;
        - ``appointment_date`` - дата приема;
        Метод возвращает ``False`` если донора не существует.
        '''
        
        if not self.is_donor_exists(id=id, telegram_id=telegram_id, number=number, email=email):
            return False
        
        if self.is_registered_donor_appointment(id=id, telegram_id=telegram_id, number=number, email=email):
            return False
        
        donor = self.get_donor_by(id=id)
        
        query = 'INSERT INTO data_blood.appointment ("ID", "clinic_ID", "donor_number_ID", "status_ID", "registration_date", "appointment_date", "analysis_file_path") VALUES (%s, %s, %s, %s, %s, %s, %s)'
        self.__cursor.execute(query, (self.get_next_row_id(table="data_blood.appointment"), clinic_id, donor.get_number_id(), 3, registration_date, appointment_date, "aboba.txt"))
        
        self.__connection.commit()
        
        return True
         
    def set_user_language(self, user_id: Union[int, str], language: str):
        if (not str(user_id) in self.languages_cache) or (self.languages_cache[str(user_id)] != language):
            self.languages_cache[str(user_id)] = language
            json.dump(self.languages_cache, open("bot/cache/user_languages.json", "w", encoding="UTF-8"))
        
    def get_user_language(self, user_id: Union[int, str]) -> str:
        return self.languages_cache[str(user_id)] if str(user_id) in self.languages_cache else cfg.DEFAULT_LANGUAGE
    
    def set_user_notifications(self, user_id: Union[int, str], option: bool):
        if (not str(user_id) in self.notifications_cache) or (self.notifications_cache[str(user_id)] != option):
            self.notifications_cache[str(user_id)] = option
            json.dump(self.notifications_cache, open("bot/cache/user_notifications.json", "w", encoding="UTF-8"))
            
    def get_user_notifications(self, user_id: Union[int, str]) -> bool:
        return self.notifications_cache[str(user_id)] if str(user_id) in self.notifications_cache else True
            
    def get_notifications_list(self):
        return self.notifications_cache
    
    def setup_database(self):
        
        print("\t\tНАСТРОЙКА БАЗЫ ДАННЫХ")
        print("Выполняется заполнение таблиц стандартными значениями")
        
        self.add_bloods()
        print("Таблица крови заполнена!")
        
        self.add_languages()
        print("Таблица языков заполнена!")
        
        self.add_statuses()
        print("Таблица статусов заполнена!")
        
        self.add_streets()
        print("Таблица улиц заполнена!")
        
        self.add_areas()
        print("Таблица ХЗ запонена!")
        
        self.add_regions()
        print("Таблица регионов заполнена!")
        
        self.add_cities()
        print("Таблица городов заполнена!")
        
        self.add_addresses()
        print("Таблица адресов заполнена!")
        
        self.add_clinics()
        print("Таблица клиник заполнена!")
        
        self.add_genders()
        print("Таблица гендеров заполнена!")