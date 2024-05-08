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
    
    def get_next_donor_id(self) -> int:
        
        '''
        Получение последнего доступного номера в таблице ``donor``.
        '''
        
        query = 'SELECT "ID" FROM donor.donor ORDER BY "ID" DESC'
        self.__cursor.execute(query)
        
        data = self.__cursor.fetchone()
        
        return 1 if data is None else data[0] + 1
    
    def is_donor_exists(self, id: int=-1, telegram_id: int=-1) -> bool:
        
        '''
        Проверка существует ли донор. В качестве параметра передается одно из двух значений:
        - ``id`` - номер донора в БД; 
        - ``telegram_id`` - номер профиля Телеграма пользоваля.\n
        Метод возвращает либо ``True``, либо ``False``.
        '''
        
        query = 'SELECT * FROM donor.donor WHERE donor."ID" = %s OR donor."telegram_ID" = %s'
        self.__cursor.execute(query, (id, telegram_id))
        
        data = self.__cursor.fetchone()
        is_exists = data is not None
        
        return is_exists
        
    def get_donor(self, id: int=-1, telegram_id: int=-1) -> Union[Donor, bool]:
        
        '''
        Сформировать объект ``Donor`` по данным из БД, если донор существует. В качестве параметра передается одно из двух значений:
        - ``id`` - номер донора в БД; 
        - ``telegram_id`` - номер профиля Телеграма пользоваля.\n 
        Возвращает ``False`` если донора не существует.
        '''
        
        query = 'SELECT donors.*, numbers."ID" AS number_ID, numbers.number AS number FROM donor.donor as donors, number_telephone.donor_number AS numbers WHERE donors."ID" = numbers."donor_ID" AND (donor."ID" = %s OR donor."telegram_ID" = %s)'
        self.__cursor.execute(query, (id, telegram_id))
        
        data = self.__cursor.fetchone()
        
        return Donor(data=data) if data is not None else False
    
    def get_donors(self) -> list[Donor]:
        
        '''
        Получить список всех доноров в виде объекта ``Donor``, существующих в БД.
        '''
        
        query = 'SELECT donors.*, numbers."ID" AS number_ID, numbers.number AS number FROM donor.donor as donors, number_telephone.donor_number AS numbers WHERE donors."ID" = numbers."donor_ID"'
        self.__cursor.execute(query)
        
        data = self.__cursor.fetchall()

        for i, donor_data in enumerate(data, start=0):
            data[i] = Donor(data=donor_data)
        
        return data
    
    # ПЕРЕСМОТРЕТЬ ПЕРЕДЕЛАТЬ
    def register_donor(self, donor: Donor) -> bool:
        
        '''
        Регистрация донора и добавление его в БД. Если донор уже существует метод вернет ``False``, в случае успешного выполнения будет возвращено значение ``True``.
        '''
        
        is_exists = self.is_donor_exists(id=donor.get_telegram())
        
        if is_exists:
            return False
        
        donor.set_ID(id=self.get_next_donor_id())

        # new_phone_id = self.get_last_id_phone()[0] + 1 
        # new_user_id = self.get_last_id_user()[0] + 1
        
        # query = 'INSERT INTO "donor".donor ("ID", "name_donor", "surname_donor", "date_of_birth", "gender_ID", "password", "language_ID") SELECT %s, %s, %s, %s, %s, %s, %s WHERE NOT EXISTS ( SELECT * FROM "numberTelephone".number_tel_don WHERE number = %s)'
        # self.__cursor.execute(query, (new_user_id, name, surname, date_of_birth, gender_id, password, language, user_phone))
        
        # query = 'INSERT INTO "numberTelephone".number_tel_don ("ID", "donor_ID", "number") SELECT %s, %s, %s WHERE NOT EXISTS (SELECT "donor_ID" FROM "numberTelephone".number_tel_don WHERE "donor_ID" = %s)'
        # self.__cursor.execute(query, (new_phone_id, new_user_id, user_phone, new_user_id)) 
        
        # self.__connection.commit()
    
    def get_donor_by_userid(self, user_id: str) -> Union[tuple, bool]:
        
        user_phone = self.get_user_phone(user_id=user_id)
        
        if user_phone:
            query = 'SELECT * FROM "donor".donor JOIN "numberTelephone".number_tel_don ON donor."ID" = number_tel_don."donor_ID" WHERE number_tel_don.number = %s'
            self.__cursor.execute(query, (user_phone, ))
            
            data = self.__cursor.fetchone()
            
            return data
        else:
            return False
    
    def get_donor_by_phone(self, user_phone: str) -> Union[tuple, bool]:
        query = 'SELECT * FROM "donor".donor JOIN "numberTelephone".number_tel_don ON donor.ID = number_tel_don."donor_ID" WHERE number_tel_don.number = %s'
        self.__cursor.execute(query, (user_phone, ))
        
        data = self.__cursor.fetchone()
        
        return data or False
        
    def register_donor_appointment(self, user_id: Union[int, str], clinic_id: Union[int, str], registration_date: str, appointment_date: str):
        
        user_phone_id = self.get_user_phone_id(user_id=user_id)
        
        if user_phone_id:
        
            query = 'INSERT INTO data_blood.appointment ("clinic_ID", "donor_tel_ID", "status_ID", "registration_date", "appointment_date", "analysis_file_path") SELECT %s, %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT * FROM data_blood.appointment WHERE "donor_tel_ID" = %s AND "status_ID" = 3)'
            self.__cursor.execute(query, (clinic_id, user_phone_id, 3, registration_date, appointment_date, "file/file.txt", user_phone_id)) 
            
            self.__connection.commit()
        
         
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
    
    def set_user_phone(self, user_id: Union[int, str], user_phone: str):
        if (not str(user_id) in self.phones_cache) or (self.phones_cache[str(user_id)] != user_phone):
            self.phones_cache[str(user_id)] = user_phone.replace("+", "").replace(" ", "")
            json.dump(self.phones_cache, open("bot/cache/user_phones.json", "w", encoding="UTF-8"))
            
    def get_user_phone(self, user_id: Union[int, str]):
        return self.phones_cache[str(user_id)] if str(user_id) in self.phones_cache else False
    
    def get_user_phone_id(self, user_id: Union[int, str]):
        user_phone = self.get_user_phone(user_id=user_id)
        
        query = 'SELECT "ID" FROM "numberTelephone".number_tel_don WHERE number = %s'
        self.__cursor.execute(query, (user_phone, ))
        
        data = self.__cursor.fetchone()
        
        return data or False
    
    def get_last_id_phone(self) -> int:
        
        query = 'SELECT "ID" FROM "numberTelephone".number_tel_don ORDER BY "ID"'
        self.__cursor.execute(query)
        
        data = self.__cursor.fetchone()
        
        return data or (0, )
    
    def get_last_id_user(self) -> int:
        
        query = 'SELECT "ID" FROM "donor".donor ORDER BY "ID"'
        self.__cursor.execute(query)
        
        data = self.__cursor.fetchone()
        
        return data or (0, )
    
    def get_clinics(self):
        query = 'SELECT "address_ID" FROM data_blood.clinic ORDER BY "ID"'
        self.__cursor.execute(query)
        
        data = self.__cursor.fetchall()
        
        return data or False
    
    def get_donor_appointments(self, user_id: Union[int, str]):
        
        user_phone = self.get_user_phone(user_id=user_id)
        
        query = 'SELECT appointment.* FROM data_blood.appointment JOIN "numberTelephone".number_tel_don ON appointment."donor_tel_ID" = number_tel_don."donor_ID" WHERE number_tel_don.number = %s AND NOT appointment."status_ID" = 3'
        self.__cursor.execute(query, (user_phone, ))
        
        data = self.__cursor.fetchall()
        
        return data or False
    
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