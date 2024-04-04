import psycopg2 as psql
import config as cfg
import json

from typing import Union

from src.classes.Singleton import Singleton

class DatabaseController(metaclass=Singleton):
    def __init__(self):
        
        self.languages_cache = json.load(open("bot/cache/user_languages.json", "r", encoding="UTF-8"))
        self.notifications_cache = json.load(open("bot/cache/user_notifications.json", "r", encoding="UTF-8"))
        
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
        
        query = 'DELETE FROM crm.blood'
        
        self.__cursor.execute(query)
        
        query = 'INSERT INTO crm.blood ("ID", "blood_name", "rh_factor") VALUES (%s, %s, %s)'
        
        self.__cursor.executemany(query, cfg.BLOODS)
        self.__connection.commit()
        
    def add_languages(self):
        
        query = 'DELETE FROM crm.language'
        
        self.__cursor.execute(query)
        
        query = 'INSERT INTO crm.language ("ID", "language_name") VALUES (%s, %s)'
        
        self.__cursor.executemany(query, cfg.LANGUAGES)
        self.__connection.commit()
        
    def add_cities(self):
        
        query = 'DELETE FROM crm.city'
        
        self.__cursor.execute(query)
        
        query = 'INSERT INTO crm.city ("ID", "city_name") VALUES (%s, %s)'
        
        self.__cursor.executemany(query, cfg.CITIES)
        self.__connection.commit()
        
    def add_regions(self):
        
        query = 'DELETE FROM crm.region'
        
        self.__cursor.execute(query)
        
        query = 'INSERT INTO crm.region ("ID", "region_name") VALUES (%s, %s)'
        
        self.__cursor.executemany(query, cfg.REGIONS)
        self.__connection.commit()
        
    def add_streets(self):
        
        query = 'DELETE FROM crm.street'
        
        self.__cursor.execute(query)
        
        query = 'INSERT INTO crm.street ("ID", "street_name") VALUES (%s, %s)'
        
        self.__cursor.executemany(query, cfg.STREETS)
        self.__connection.commit()
        
    def add_areas(self):
        
        query = 'DELETE FROM crm.area'
        
        self.__cursor.execute(query)
        
        query = 'INSERT INTO crm.area ("ID", "area_name") VALUES (%s, %s)'
        
        self.__cursor.executemany(query, cfg.AREAS)
        self.__connection.commit() 
        
    def add_addresses(self):
        
        query = 'DELETE FROM crm.address'
        
        self.__cursor.execute(query)
        
        query = 'INSERT INTO crm.address ("ID", "region_ID", "city_ID", "area_ID", "street_ID") VALUES (%s, %s, %s, %s, %s)'
        
        self.__cursor.executemany(query, cfg.ADDRESSES)
        self.__connection.commit()
        
    def add_statuses(self):
        
        query = 'DELETE FROM crm.status'
        
        self.__cursor.execute(query)
        
        query = 'INSERT INTO crm.status ("ID", "status_name") VALUES (%s, %s)'
        
        self.__cursor.executemany(query, cfg.STATUSES)
        self.__connection.commit()
        
    def add_clinics(self):
        
        query = 'DELETE FROM crm.clinic'
        
        self.__cursor.execute(query)
        
        query = 'INSERT INTO crm.clinic ("ID", "clinic_name", "working_hours", "address_ID") VALUES (%s, %s, %s, %s)'
        
        self.__cursor.executemany(query, cfg.CLINICS)
        self.__connection.commit()
        
    def add_doctors(self):
        
        query = 'DELETE FROM crm.doctor'
        
        self.__cursor.execute(query)
        
        query = 'INSERT INTO crm.doctor ("ID", "doctor_name", "specialization", "address_ID", "clinic_ID") VALUES (%s, %s, %s, %s, %s)'
        
        self.__cursor.executemany(query, cfg.DOCTORS)
        self.__connection.commit()
    
    def get_donor(self, user_id: Union[int, str]) -> Union[tuple, bool]:

        query = 'SELECT * FROM crm.donor WHERE "ID" = %s'

        self.__cursor.execute(query, (user_id, ))
        data = self.__cursor.fetchone()
        
        return data or False
    
    def register_donor(self, id: Union[int, str], name: str, date: str, gender: str, language: int, blood: int):
        
        query = 'INSERT INTO crm.donor ("ID", "donor_name", "date_of_birth", "gender", "language_ID", "blood_ID") SELECT %s, %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT "ID" FROM crm.donor WHERE "ID" = %s)'
        
        self.__cursor.execute(query, (id, name, date, gender, language, blood, id))
        self.__connection.commit()
        
    def delete_donor(self, id: Union[int, str]):
        
        query = 'DELETE FROM crm.donor WHERE "ID" = %s'
        
        self.__cursor.execute(query, (id, ))
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
        
        self.add_doctors()
        print("Таблица докторов заполнена!")