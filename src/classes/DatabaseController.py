import psycopg2 as psql
import config as cfg

from typing import Union

from src.classes.Singleton import Singleton

class DatabaseController(metaclass=Singleton):
    def __init__(self):
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
        
    def get_user(self, id: Union[int, str]) -> Union[tuple, bool]:
        
        self.connect()

        query = 'SELECT * FROM crm.donor WHERE "ID" = %s'

        self.__cursor.execute(query, (id, ))
        data = self.__cursor.fetchone()
        
        self.disconnect()
        
        return data or False
    
    def add_user(self, id: Union[int, str], name: str, date: str, gender: str, language: int, blood: int):
        
        self.connect()
        
        query = 'INSERT INTO crm.donor ("ID", "donor_name", "date_of_birth", "gender", "language_ID", "blood_ID") VALUES (%s, %s, %s, %s, %s, %s)'
        
        self.__cursor.execute(query, (id, name, date, gender, language, blood))
        self.__connection.commit()
        
        self.disconnect()
        
    def delete_user(self, id: Union[int, str]):
        
        self.connect()
        
        query = 'DELETE FROM crm.donor WHERE "ID" = %s'
        
        self.__cursor.execute(query, (id, ))
        self.__connection.commit()
        
        self.disconnect()
        
    def set_user_language(self, ind: Union[int, str], language_ID: int):
        self.connect()
        
        self.disconnect()
        
    def setup_database(self):
        
        self.add_bloods()
        self.add_languages()
        
        self.add_streets()
        self.add_areas()
        self.add_regions()
        self.add_cities()
        self.add_addresses()