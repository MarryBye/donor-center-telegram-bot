import psycopg2 as psql
import psycopg2.extras as psql_extra
import config as cfg
import json

from typing import Union

from src.classes.Singleton import Singleton
from src.classes.Donor import Donor
from src.classes.Appointment import Appointment
from src.classes.Crypto import Crypto


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
        self.__cursor = self.__connection.cursor(cursor_factory=psql_extra.RealDictCursor)

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

        query = ('INSERT INTO data_blood.address ("ID", "region_ID", "city_ID", "area_ID", "street_ID", '
                 '"house_number") VALUES (%s, %s, %s, %s, %s, %s)')
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

        query = ('INSERT INTO data_blood.clinic ("ID", "clinic_name", "address_ID", "working_hours") VALUES (%s, %s, '
                 '%s, %s)')
        self.__cursor.executemany(query, cfg.CLINICS)

        self.__connection.commit()

    def get_next_row_id(self, table: str) -> int:

        """

        Получение последнего доступного номера в таблице, указанной в аргументе ``table``.\n Метод возвращает число -
        следующая свободная строка в указанной таблице.\n\n ВНИМАНИЕ! Метод использует НЕБЕЗОПАСНЫЕ (подверженные SQL
        инжекции способы подстановки названия таблицы. Ни при каких обстоятельствах не позволять пользователю вводить
        самостоятельно название таблицы или давать возможность воспользоваться методом)

        """

        query = 'SELECT "ID" FROM %s ORDER BY "ID" DESC' % table
        self.__cursor.execute(query)

        data = self.__cursor.fetchone()

        return 1 if data is None else data["ID"] + 1

    def get_donor_by(self, db_id: int = -1, telegram_id: int = -1, number: str = "-1", email: str = "-1") -> Donor:

        """
        Сформировать объект ``Donor`` по данным из БД. В качестве параметров передается одно из или несколько следующих
        значений:
        - ``id`` - номер донора в БД;
        - ``telegram_id`` - номер профиля Телеграма пользоваля;
        - ``number`` - номер телефона пользователя;
        - ``email`` - электронная почта пользователя.\n
        Метод возвращает объект ``Donor`` если донор существует или нет, но во втором случае все данные про донора будут
        равняться ``None``.
        """

        query = ('SELECT donors.*, numbers."ID" AS "number_ID", numbers.number AS number FROM donor.donor as donors, '
                 'number_telephone.donor_number AS numbers WHERE donors."ID" = numbers."donor_ID" AND (donors."ID" = '
                 '%s OR donors."telegram_ID" = %s OR numbers.number = %s OR donors.email = %s)')
        self.__cursor.execute(query, (db_id, telegram_id, number, email))

        data = self.__cursor.fetchone()

        return Donor(data=data) if data is not None else Donor()

    def get_donors(self) -> list[Donor]:

        """
        Получить список всех доноров существующих в БД в виде объектов ``Donor``.
        """

        query = ('SELECT donors.*, numbers."ID" AS number_ID, numbers.number AS number FROM donor.donor as donors, '
                 'number_telephone.donor_number AS numbers WHERE donors."ID" = numbers."donor_ID"')
        self.__cursor.execute(query)

        data = self.__cursor.fetchall()

        for i, donor_data in enumerate(data, start=0):
            data[i] = Donor(data=donor_data)

        return data

    def register_donor(self, donor: Donor) -> bool:

        """
        Регистрация донора и добавление его в БД если его в ней нет. В качестве аргумента принимает:
        - ``donor`` - объект ``Donor`` с информацией про нового донора.\n
        В случае успешного выполнения будет возвращено значение ``True``, в ином случае ``False``.
        """

        if not self.get_donor_by(db_id=donor.get_id(), telegram_id=donor.get_telegram(), number=donor.get_number(),
                                 email=donor.get_email()).is_empty():
            return False

        try:
            donor.set_id(db_id=self.get_next_row_id(table="donor.donor"))
            donor.set_number_id(number_id=self.get_next_row_id(table="number_telephone.donor_number"))

            if not donor.is_full():
                return False

            query = ('INSERT INTO donor.donor ("ID", "name_donor", "surname_donor", "date_of_birth", "gender_ID", '
                     '"email", "telegram_ID", "password", "language_ID") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
            self.__cursor.execute(query, (
                donor.get_id(),
                donor.get_name(),
                donor.get_surname(),
                donor.get_birthdate(),
                donor.get_gender(),
                donor.get_email(),
                donor.get_telegram(),
                Crypto().code(donor.get_password()),
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
        except:
            return False

    def is_registered_donor_appointment(self, donor: Donor) -> bool:

        """
        Узнать, зарегистрирован ли донор на прием (прием с статусом "3"). В качестве параметра принимает:
        - ``donor`` - объект ``Donor`` с информацией про донора.\n
        Если донор зарегистрирован на прием будет возвращено значение ``True``, в ином случае ``False``.
        """

        query = ('SELECT appointments."ID" FROM donor.donor AS donors, number_telephone.donor_number AS numbers, '
                 'data_blood.appointment AS appointments WHERE appointments."status_ID" = 3 AND '
                 'appointments."donor_number_ID" = numbers."ID" AND numbers."donor_ID" = donors."ID" AND (donors."ID" '
                 '= %s OR donors."telegram_ID" = %s OR numbers.number = %s OR donors.email = %s)')
        self.__cursor.execute(query, (donor.get_id(), donor.get_telegram(), donor.get_number(), donor.get_email()))

        data = self.__cursor.fetchone()
        is_registered = data is not None

        return is_registered

    def get_donor_appointments(self, donor: Donor, need_status: int = None, need_registration_date: str = None,
                               need_appointment_date: str = None, only_last: bool = True) -> Union[Appointment, bool]:

        """
        Сформировать объект ``Appointment`` по данным из БД, если донор существует. В качестве параметра принимает:
        - ``donor`` - объект ``Donor`` с информацией про донора.\n
        Далее идут необязательные параметры для фильтрации данных:
        - ``need_status`` - с каким статусом искать приемы. Если не указано, то возвращаются все приемы;
        - ``only_last`` - получить только последнюю запись из БД;
        - ``need_appointment_date`` - получить только с определенной датой встречи;
        - ``need_registration_date`` - получить только с определенной датой регистрации встречи.\n
        Метод возвращает ``False`` если донора не существует.
        """

        additional_filters = ''
        additional_filters_args = []

        if need_status is not None:
            additional_filters += ' AND appointments."status_ID" = %s'
            additional_filters_args.append(need_status)
        if need_registration_date is not None:
            additional_filters += ' AND appointments.registration_date = %s'
            additional_filters_args.append(need_registration_date)
        if need_appointment_date is not None:
            additional_filters += ' AND appointments.appointment_date = %s'
            additional_filters_args.append(need_appointment_date)

        query = ('SELECT appointments.* FROM donor.donor AS donors, number_telephone.donor_number AS numbers, '
                 'data_blood.appointment AS appointments WHERE appointments."donor_number_ID" = numbers."ID" AND '
                 'numbers."donor_ID" = donors."ID" AND (donors."ID" = %s OR donors."telegram_ID" = %s OR '
                 'numbers.number = %s OR donors.email = %s)') + additional_filters
        self.__cursor.execute(query, (
            donor.get_id(), donor.get_telegram(), donor.get_number(), donor.get_email(), *additional_filters_args))

        if only_last:
            data = self.__cursor.fetchone()
            return Appointment(data=data) if data is not None else Appointment()
        else:
            data = self.__cursor.fetchall()
            for i, data_component in enumerate(data, start=0):
                data[i] = Appointment(data=data_component)
            return data if data is not None else []

    def register_donor_appointment(self, appointment: Appointment, donor: Donor):

        """
        Зарегистрировать донора на прием. Принимает следующие аргументы:
        - ``appointment`` - принимает объект ``Appointment`` с данными про новый прием;
        - ``donor`` - принимает объект ``Donor`` с данными про донора.\n
        Метод возвращает ``False`` если донор уже зарегистрирован на прием или нет данных о доноре.
        """

        if self.is_registered_donor_appointment(donor=donor):
            return False

        if donor.get_number_id() is None:
            return False

        appointment.set_id(db_id=self.get_next_row_id(table="data_blood.appointment"))
        appointment.set_donor_number_id(donor_number_id=donor.get_number_id())
        appointment.set_status_id(status_id=3)

        if not appointment.is_full():
            return False

        try:

            query = ('INSERT INTO data_blood.appointment ("ID", "clinic_ID", "donor_number_ID", "status_ID", '
                     '"registration_date", "appointment_date", "analysis_file_path") VALUES (%s, %s, %s, %s, %s, %s, '
                     '%s)')
            self.__cursor.execute(query, (
                appointment.get_id(),
                appointment.get_clinic_id(),
                appointment.get_donor_number_id(),
                appointment.get_status_id(),
                appointment.get_registration_date(),
                appointment.get_appointment_date(),
                appointment.get_analysis_file_path()
            )
                                  )

            self.__connection.commit()

            return True

        except:
            return False

    def change_donor_appointment_status(self, appointment_id: int, donor: Donor):
        pass

    def delete_donor(self, donor: Donor):

        """
        Удалить донора из таблицы доноров, а также его номер телефона, который к нему привязан.Принимает следующие
        аргументы:
        - ``donor`` - принимает объект ``Donor`` с данными про донора.\n
        Метод возвращает ``False`` если донора удалить не получилось.
        """

        if not donor.is_full():
            return False

        query = ('DELETE FROM donor.donor as donors WHERE donors."ID" = %s OR donors."telegram_ID" = %s OR '
                 'donors.email = %s')
        self.__cursor.execute(query, (donor.get_id(), donor.get_telegram(), donor.get_email()))

        query = ('DELETE FROM number_telephone.donor_number AS numbers WHERE numbers.number = %s OR numbers."ID" = %s '
                 'OR numbers."donor_ID" = %s')
        self.__cursor.execute(query, (donor.get_number(), donor.get_number_id(), donor.get_id()))

        query = 'DELETE FROM data_blood.appointment AS appointments WHERE appointments."donor_number_ID" = %s'
        self.__cursor.execute(query, (donor.get_id(),))

        self.__connection.commit()

        return True

    def delete_donor_appointment(self, donor: Donor, appointment: Appointment):
        pass

    def set_user_language(self, donor: Donor, language: str, only_cache: bool = False):

        """
        Устанавливает значение языка в БД и кеше бота чтобы в дальнейшем при запросах языка не обращаться в БД.
        """

        for language in cfg.LANGUAGES:
            if language in language:
                language = language[0]
            else:
                return False

        if (not str(donor.get_telegram()) in self.languages_cache) or (
                self.languages_cache[str(donor.get_telegram())] != language):

            if not donor.is_full() and not only_cache:
                return False

            try:
                if not only_cache:
                    query = ('UPDATE donor.donor AS donors SET donors.language_ID = %s WHERE donors."ID" = %s OR '
                             'donors."telegram_ID" = %s OR donors.email = %s')
                    self.__cursor.execute(query, (language, donor.get_id(), donor.get_telegram(), donor.get_email()))

                    self.__connection.commit()

                self.languages_cache[str(donor.get_telegram())] = language
                json.dump(self.languages_cache, open("bot/cache/user_languages.json", "w", encoding="UTF-8"))

                return True
            except:
                return False

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
