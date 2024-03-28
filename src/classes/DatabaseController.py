import psycopg2 as psql
import config as cfg

from typing import Union

from src.classes.Singleton import Singleton

class DatabaseController(metaclass=Singleton):
    def __init__(self):
        
        self.cache = {}
        
        self.__connection = None
        self.__cursor = None
        
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
        
        self.connect()
        
        query = 'DELETE FROM crm.blood'
        
        self.__cursor.execute(query)
        
        bloods = (
            (1, "AB", "+"),
            (2, "AB", "-"),
            (3, "A", "+"),
            (4, "A", "-"),
            (5, "B", "+"),
            (6, "B", "-"),
            (7, "O", "+"),
            (8, "O", "-")
        )
        
        query = 'INSERT INTO crm.blood ("ID", "blood_name", "rh_factor") VALUES (%s, %s, %s)'
        
        self.__cursor.executemany(query, bloods)
        self.__connection.commit()
        
        self.disconnect()
        
    def add_languages(self):
        
        self.connect()
        
        query = 'DELETE FROM crm.language'
        
        self.__cursor.execute(query)
        
        languages = (
            (1, "cn-CN"),
            (2, "de-DE"),
            (3, "en-EN"),
            (4, "fr-FR"),
            (5, "ru-RU"),
            (6, "uk-UK")
        )
        
        query = 'INSERT INTO crm.language ("ID", "language_name") VALUES (%s, %s)'
        
        self.__cursor.executemany(query, languages)
        self.__connection.commit()
        
        self.disconnect()
        
    def add_cities(self):
        
        self.connect()
        
        query = 'DELETE FROM crm.city'
        
        self.__cursor.execute(query)
        
        cities = (
            (1, "Odessa"),
            (2, "Kiyv"),
            (3, "Lviv")
        )
        
        query = 'INSERT INTO crm.city ("ID", "city_name") VALUES (%s, %s)'
        
        self.__cursor.executemany(query, cities)
        self.__connection.commit()
        
        self.disconnect()
        
    def add_regions(self):
        
        self.connect()
        
        query = 'DELETE FROM crm.region'
        
        self.__cursor.execute(query)
        
        regions = (
            (1, "Odes`ka Oblast"),
            (2, "Kiyvska Oblast"),
            (3, "Lvivska Oblast")
        )
        
        query = 'INSERT INTO crm.region ("ID", "region_name") VALUES (%s, %s)'
        
        self.__cursor.executemany(query, regions)
        self.__connection.commit()
        
        self.disconnect()
        
    def add_streets(self):
        
        self.connect()
        
        query = 'DELETE FROM crm.street'
        
        self.__cursor.execute(query)
        
        streets = (
            (1, "Generala Petrova, 66"),
            (2, "Akademika Koroliova, 3"),
            (3, "Jopa Bobra, 8"),
            (4, "Abobakar pepe abobakar, 88")
        )
        
        query = 'INSERT INTO crm.street ("ID", "street_name") VALUES (%s, %s)'
        
        self.__cursor.executemany(query, streets)
        self.__connection.commit()
        
        self.disconnect()
        
    def add_areas(self):
        
        self.connect()
        
        query = 'DELETE FROM crm.area'
        
        self.__cursor.execute(query)
        
        areas = (
            (1, "Area1"),
            (2, "Area2"),
            (3, "Area3"),
            (4, "Area4"),
            (5, "Area5"),
            (6, "Area6")
        )
        
        query = 'INSERT INTO crm.area ("ID", "area_name") VALUES (%s, %s)'
        
        self.__cursor.executemany(query, areas)
        self.__connection.commit() 
        
        self.disconnect()
        
    def add_addresses(self):
        
        self.connect()
        
        query = 'DELETE FROM crm.address'
        
        self.__cursor.execute(query)
        
        addresses = (
            (1, 2, 2, 2, 2),
            (2, 2, 3, 1, 2),
            (3, 1, 1, 1, 1),
            (4, 1, 2, 1, 3),
            (5, 2, 1, 2, 1)
        )
        
        query = 'INSERT INTO crm.address ("ID", "region_ID", "city_ID", "area_ID", "street_ID") VALUES (%s, %s, %s, %s, %s)'
        
        self.__cursor.executemany(query, addresses)
        self.__connection.commit()
        
        self.disconnect()
        
    def add_statuses(self):
        
        self.connect()
        
        query = 'DELETE FROM crm.status'
        
        self.__cursor.execute(query)
        
        statuses = (
            (1, "Success"),
            (2, "Unsuccess")
        )
        
        query = 'INSERT INTO crm.status ("ID", "status_name") VALUES (%s, %s)'
        
        self.__cursor.executemany(query, statuses)
        self.__connection.commit()
        
        self.disconnect()
        
    def add_clinics(self):
        
        self.connect()
        
        query = 'DELETE FROM crm.clinic'
        
        self.__cursor.execute(query)
        
        clinics = (
            (1, "Клиника АДЫН", "12:00:00", 1),
            (2, "Клиника СЕКОНД", "15:00:00", 2),
            (3, "Клиника ТРЫЫЫЫ", "13:00:00", 3),
            (4, "Клиника ЧОТЫРИ", "14:00:00", 4),
            (5, "Клиника ФАААААЙФФВВВ", "16:30:00", 5)
        )
        
        query = 'INSERT INTO crm.clinic ("ID", "clinic_name", "working_hours", "address_ID") VALUES (%s, %s, %s, %s)'
        
        self.__cursor.executemany(query, clinics)
        self.__connection.commit()
        
        self.disconnect()
        
    def add_doctors(self):
        
        self.connect()
        
        query = 'DELETE FROM crm.doctor'
        
        self.__cursor.execute(query)
        
        doctors = (
            (1, "Иван", "Пипабоди", 1, 1),
            (2, "Ванька", "Фистер", 2, 2),
            (3, "Женя", "Эйналщик", 3, 3),
            (4, "Михаил", "Темщик-Схемщик", 4, 4),
            (5, "Кчаур", "Автобус", 5, 5)
        )
        
        query = 'INSERT INTO crm.doctor ("ID", "doctor_name", "specialization", "address_ID", "clinic_ID") VALUES (%s, %s, %s, %s, %s)'
        
        self.__cursor.executemany(query, doctors)
        self.__connection.commit()
        
        self.disconnect() 
        
    def get_user(self, user_id: Union[int, str]) -> Union[tuple, bool]:
        
        self.connect()

        query = 'SELECT * FROM crm.donor WHERE "ID" = %s'

        self.__cursor.execute(query, (user_id, ))
        data = self.__cursor.fetchone()
        
        self.disconnect()
        
        return data or False
    
    def add_user(self, id: Union[int, str], name: str, date: str, gender: str, language: int, blood: int):
        
        self.connect()
        
        query = 'INSERT INTO crm.donor ("ID", "donor_name", "date_of_birth", "gender", "language_ID", "blood_ID") SELECT %s, %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT "ID" FROM crm.donor WHERE "ID" = %s)'
        
        self.__cursor.execute(query, (id, name, date, gender, language, blood, id))
        self.__connection.commit()
        
        self.disconnect()
        
    def delete_user(self, id: Union[int, str]):
        
        self.connect()
        
        query = 'DELETE FROM crm.donor WHERE "ID" = %s'
        
        self.__cursor.execute(query, (id, ))
        self.__connection.commit()
        
        self.disconnect()
        
    def set_user_language(self, user_id: Union[int, str], language: str):
        self.connect()
        
        query = 'SELECT "ID" FROM crm.language WHERE language."language_name" = %s'
        
        self.__cursor.execute(query, (language, ))
        data = self.__cursor.fetchone()[0]
        
        query = 'UPDATE crm.donor SET "language_ID" = %s WHERE "ID" = %s'
        
        self.__cursor.execute(query, (data, user_id))
        self.__connection.commit()
        
        self.disconnect()
        
    def get_user_language(self, user_id: Union[int, str]) -> str:
        '''Повертає назву мови, яку хоче використовувати користувач. Назва співпадає з назвами файлів у директорії lang.'''
        
        self.connect()
        
        query = 'SELECT language_name FROM crm.donor, crm.language WHERE donor."language_ID" = language."ID" AND donor."ID" = %s'
        
        self.__cursor.execute(query, (user_id, ))
        data = self.__cursor.fetchone()
        
        self.disconnect()
        
        return data[0] if type(data) == tuple and len(data) > 0 else cfg.DEFAULT_LANGUAGE
        
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