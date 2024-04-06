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
        
        query = 'DELETE FROM "dataBlood".blood_and_components'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO "dataBlood".blood_and_components ("ID", "blood_and_comp_name") VALUES (%s, %s)'
        self.__cursor.executemany(query, cfg.BLOODS)
        
        self.__connection.commit()
        
    def add_languages(self):
        
        query = 'DELETE FROM "donor".language'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO "donor".language ("ID", "language") VALUES (%s, %s)'
        self.__cursor.executemany(query, cfg.LANGUAGES)
        
        self.__connection.commit()
        
    def add_cities(self):
        
        query = 'DELETE FROM "dataBlood".city'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO "dataBlood".city ("ID", "city_name") VALUES (%s, %s)'
        self.__cursor.executemany(query, cfg.CITIES)
        
        self.__connection.commit()
        
    def add_regions(self):
        
        query = 'DELETE FROM "dataBlood".region'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO "dataBlood".region ("ID", "region_name") VALUES (%s, %s)'
        self.__cursor.executemany(query, cfg.REGIONS)
        
        self.__connection.commit()
        
    def add_streets(self):
        
        query = 'DELETE FROM "dataBlood".street'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO "dataBlood".street ("ID", "street_name") VALUES (%s, %s)'
        self.__cursor.executemany(query, cfg.STREETS)
        
        self.__connection.commit()
        
    def add_areas(self):
        
        query = 'DELETE FROM "dataBlood".area'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO "dataBlood".area ("ID", "area_name") VALUES (%s, %s)'
        self.__cursor.executemany(query, cfg.AREAS)
        
        self.__connection.commit() 
        
    def add_addresses(self):
        
        query = 'DELETE FROM "dataBlood".address'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO "dataBlood".address ("ID", "region_ID", "city_ID", "area_ID", "street_ID") VALUES (%s, %s, %s, %s, %s)'
        self.__cursor.executemany(query, cfg.ADDRESSES)
        
        self.__connection.commit()
        
    def add_statuses(self):
        
        query = 'DELETE FROM "dataBlood".status_appointment'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO "dataBlood".status_appointment ("ID", "name_status") VALUES (%s, %s)'
        self.__cursor.executemany(query, cfg.STATUSES)
        
        self.__connection.commit()
        
    def add_clinics(self):
        
        query = 'DELETE FROM "dataBlood".clinic'
        self.__cursor.execute(query)
        
        query = 'INSERT INTO "dataBlood".clinic ("ID", "address_ID") VALUES (%s, %s)'
        self.__cursor.executemany(query, cfg.CLINICS)
        
        self.__connection.commit()
    
    def get_donor(self, user_id: Union[int, str]) -> Union[tuple, bool]:

        query = 'SELECT * FROM "donor".donor WHERE "ID" = %s'
        self.__cursor.execute(query, (user_id, ))
        
        data = self.__cursor.fetchone()
        
        return data or False
    
    def register_donor(self, id: Union[int, str], name: str, firstname: str, language: int, phone: str):
        
        new_phone_id = self.get_last_id_phone() + 1 
        
        query = 'INSERT INTO "donor".donor ("ID", "name_donor", "first_name_donor", "language_ID") SELECT %s, %s, %s, %s WHERE NOT EXISTS (SELECT "ID" FROM "donor".donor WHERE "ID" = %s)'
        self.__cursor.execute(query, (id, name, firstname, language, id))
        
        query = 'INSERT INTO "numberTelephone".number_tel_don ("ID", "donor_ID", "number") SELECT %s, %s, %s WHERE NOT EXISTS (SELECT "donor_ID" FROM "numberTelephone".number_tel_don WHERE "donor_ID" = %s)'
        self.__cursor.execute(query, (new_phone_id, id, phone, id)) 
        
        self.__connection.commit() 
        
    def delete_donor(self, id: Union[int, str]):
        
        query = 'DELETE FROM "donor".donor WHERE "ID" = %s'
        self.__cursor.execute(query, (id, ))
        
        query = 'DELETE FROM "numberTelephone".number_tel_don WHERE "donor_ID" = %s'
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
            
    def get_last_id_phone(self) -> int:
        
        query = 'SELECT "ID" FROM "numberTelephone".number_tel_don ORDER BY "ID"'
        self.__cursor.execute(query)
        
        data = self.__cursor.fetchone()
        
        return data or 0
            
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