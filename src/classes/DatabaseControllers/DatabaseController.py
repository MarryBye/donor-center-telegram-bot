import psycopg2 as psql
import psycopg2.extras as psql_extra
import config as cfg
import json

from src.classes.Singleton import Singleton
from src.classes.Datatypes.City import City
from src.classes.Datatypes.Region import Region
from src.classes.Datatypes.Street import Street
from src.classes.Datatypes.Area import Area
from src.classes.Datatypes.Address import Address
from src.classes.Datatypes.Clinic import Clinic
from src.classes.Datatypes.Blood import Blood
from src.classes.Datatypes.Status import Status
from src.classes.Datatypes.Donor import Donor
from src.classes.Datatypes.Appointment import Appointment
from src.classes.Datatypes.Review import Review
from src.classes.Datatypes.HasBlood import HasBlood
from src.classes.Datatypes.Gender import Gender
from src.classes.Datatypes.Telephone import Telephone
from src.classes.Datatypes.Language import Language

from src.funcs.debug_print import debug_print


class DatabaseController(metaclass=Singleton):
    def __init__(self):

        self.languages_cache = json.load(open("bot/cache/user_languages.json", "r", encoding="UTF-8"))
        self.notifications_cache = json.load(open("bot/cache/user_notifications.json", "r", encoding="UTF-8"))
        self.phones_cache = json.load(open("bot/cache/user_phones.json", "r", encoding="UTF-8"))
        self.admins_cache = json.load(open("bot/cache/user_admins.json", "r", encoding="UTF-8"))

        self.connection = None
        self.cursor = None

        self.connect()

        debug_print("DatabaseController (or his subclasses) has been initialized!")

    def connect(self):
        self.connection = psql.connect(database=cfg.DATABASE_NAME,
                                       host=cfg.IP_ADDRESS,
                                       user=cfg.USERNAME,
                                       password=cfg.PASSWORD,
                                       port=cfg.PORT)
        self.cursor = self.connection.cursor(cursor_factory=psql_extra.RealDictCursor)

        debug_print("Connected to database!")

    def disconnect(self):
        self.cursor.close()
        self.connection.close()

        debug_print("Disconnected from database!")

    def get_next_row_id(self, table: str) -> int:
        """

        Получение последнего доступного номера в таблице, указанной в аргументе ``table``.\n Метод возвращает число -
        следующая свободная строка в указанной таблице.\n\n ВНИМАНИЕ! Метод использует НЕБЕЗОПАСНЫЕ (подверженные SQL
        инжекции способы подстановки названия таблицы. Ни при каких обстоятельствах не позволять пользователю вводить
        самостоятельно название таблицы или давать возможность воспользоваться методом)

        """

        query = 'SELECT "ID" FROM %s ORDER BY "ID" DESC' % table
        self.cursor.execute(query)

        data = self.cursor.fetchone()

        return 1 if data is None else data["ID"] + 1

    def get_city(self, city_id: int | str) -> City | None:

        query = 'SELECT * FROM data_blood.city AS city WHERE city."ID" = %s'
        self.cursor.execute(query, (city_id,))
        data = self.cursor.fetchone()

        return City(data=data) if data is not None else None

    def get_region(self, region_id: int | str) -> Region | None:

        query = 'SELECT * FROM data_blood.region AS region WHERE region."ID" = %s'
        self.cursor.execute(query, (region_id,))
        data = self.cursor.fetchone()

        return Region(data=data) if data is not None else None

    def get_street(self, street_id: int | str) -> Street | None:
        query = 'SELECT * FROM data_blood.street AS street WHERE street."ID" = %s'
        self.cursor.execute(query, (street_id,))
        data = self.cursor.fetchone()

        return Street(data=data) if data is not None else None

    def get_area(self, area_id: int | str) -> Area | None:

        query = 'SELECT * FROM data_blood.area AS area WHERE area."ID" = %s'
        self.cursor.execute(query, (area_id,))
        data = self.cursor.fetchone()

        return Area(data=data) if data is not None else None

    def get_address(self, address_id: int | str) -> Address | None:

        query = (
            'SELECT '
            'address."ID", '
            'address."area_ID" AS area, '
            'address."city_ID" AS city, '
            'address."region_ID" AS region, '
            'address."street_ID" AS street, '
            'address."house_number" AS house '
            'FROM data_blood.address AS address '
            'WHERE address."ID" = %s'
        )

        self.cursor.execute(query, (address_id,))
        data = self.cursor.fetchone()

        data["area"] = self.get_area(area_id=data["area"])
        data["city"] = self.get_city(city_id=data["city"])
        data["region"] = self.get_region(region_id=data["region"])
        data["street"] = self.get_street(street_id=data["street"])

        return Address(data=data) if data is not None else None

    def get_clinic(self, clinic_id: int | str) -> Clinic | None:

        query = (
            'SELECT '
            'clinic."ID", '
            'clinic."clinic_name" AS clinic_name, '
            'clinic."address_ID" AS address, '
            'clinic."working_hours" AS working_hours '
            'FROM data_blood.clinic AS clinic '
            'WHERE clinic."ID" = %s'
        )

        self.cursor.execute(query, (clinic_id,))
        data = self.cursor.fetchone()

        data["address"] = self.get_address(address_id=data["address"])
        #data["has_blood"] = self.get_has_blood(clinic_id=data["ID"])

        return Clinic(data=data) if data is not None else None

    def get_blood(self, blood_id: int | str) -> Blood | None:

        query = 'SELECT blood.* FROM data_blood.blood_and_components AS blood WHERE blood."ID" = %s'

        self.cursor.execute(query, (blood_id,))
        data = self.cursor.fetchone()

        return Blood(data=data) if data is not None else None

    def get_status(self, status_id: int | str) -> Status | None:

        query = 'SELECT status.* FROM data_blood.status_appointment AS status WHERE status."ID" = %s'

        self.cursor.execute(query, (status_id,))
        data = self.cursor.fetchone()

        return Status(data=data) if data is not None else None

    def get_review(self, review_id: int | str) -> Review | None:

        query = (
            'SELECT '
            'review."ID",'
            'review."donor_ID" AS donor,'
            'review."clinic_ID" AS clinic,'
            'review."rating",'
            'review."comment",'
            'review.date_added '
            'FROM data_blood."reviews" AS review '
            'WHERE review."ID" = %s'
        )

        self.cursor.execute(query, (review_id,))

        data = self.cursor.fetchone()

        data["donor"] = self.get_donor(db_id=data["donor"])
        data["clinic"] = self.get_clinic(clinic_id=data["clinic"])

        return Review(data=data) if data is not None else None

    def get_gender(self, gender_id: int | str) -> Gender | None:

        query = 'SELECT * FROM donor."gender" AS gender WHERE gender."ID" = %s'
        self.cursor.execute(query, (gender_id,))
        data = self.cursor.fetchone()

        return Gender(data=data) if data is not None else None

    def get_language(self, language_id: int | str) -> Language | None:

        query = 'SELECT * FROM donor."language" AS language WHERE language."ID" = %s'
        self.cursor.execute(query, (language_id,))
        data = self.cursor.fetchone()

        return Language(data=data) if data is not None else None

    def get_telephone(self, telephone_id: int | str) -> Telephone | None:

        query = (
            'SELECT '
            'number."ID",'
            'number."number" '
            'FROM number_telephone."donor_number" AS number '
            'WHERE number."ID" = %s'
        )
        self.cursor.execute(query, (telephone_id,))
        data = self.cursor.fetchone()

        return Telephone(data=data) if data is not None else None


    def get_has_blood(self, blood_id: int | str = -1, clinic_id: int | str = -1):

        query = (
            'SELECT '
            'has_blood."blood_and_comp_ID" AS blood,'
            'has_blood."clinic_ID" AS clinic,'
            'has_blood."kol" AS quantity '
            'FROM data_blood.clinic_has_blood_and_comp AS has_blood '
            'WHERE (has_blood."blood_and_comp_ID" = %s OR has_blood."clinic_ID" = %s)'
        )
        self.cursor.execute(query, (blood_id, clinic_id))

        data = self.cursor.fetchone()

        data["blood"] = self.get_blood(blood_id=data["blood"])
        data["clinic"] = self.get_clinic(clinic_id=data["clinic"])

        return HasBlood(data=data) if data is not None else None

    def get_donor(self, db_id: int = -1, telegram_id: int = -1, number: str = "-1", email: str = "-1") -> Donor | None:
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

        query = (
            'SELECT '
            'donors."ID",'
            'donors."name_donor",'
            'donors."surname_donor",'
            'donors."date_of_birth",'
            'donors."gender_ID" AS gender,'
            'donors."email",'
            'donors."telegram_ID",'
            'donors."password",'
            'donors."language_ID" AS language, '
            'numbers."ID" AS "telephone" '
            'FROM donor.donor as donors, '
            'number_telephone.donor_number AS numbers '
            'WHERE donors."ID" = numbers."donor_ID" '
            'AND '
            '(donors."ID" = %s OR donors."telegram_ID" = %s OR numbers.number = %s OR donors.email = %s)'
        )
        self.cursor.execute(query, (db_id, telegram_id, number, email))

        data = self.cursor.fetchone()

        data["telephone"] = self.get_telephone(telephone_id=data["telephone"])
        data["gender"] = self.get_gender(gender_id=data["gender"])
        data["language"] = self.get_language(language_id=data["language"])

        return Donor(data=data) if data is not None else None

    def get_donor_appointments(self, donor: Donor, need_status: int = None, need_registration_date: str = None,
                               need_appointment_date: str = None, only_last: bool = True) -> Appointment | list[Appointment] | None:

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

        query = (
            'SELECT '
            'appointments."ID",'
            'appointments."clinic_ID" AS clinic,'
            'donors."ID" AS donor,'
            'appointments."status_ID" AS status,'
            'appointments."registration_date",'
            'appointments."appointment_date",'
            'appointments."analysis_file_path" '
            'FROM '
            'donor.donor as donors, '
            'number_telephone.donor_number as numbers, '
            'data_blood.appointment as appointments '
            'WHERE '
            'appointments."donor_number_ID" = numbers."ID" '
            'AND '
            'numbers."donor_ID" = donors."ID" '
            'AND '
            '(donors."ID" = %s OR donors."telegram_ID" = %s OR numbers.number = %s OR donors.email = %s)'
        )
        self.cursor.execute(query + additional_filters, (donor.get_id(), donor.get_telegram_id(), donor.get_telephone().get_number(), donor.get_email(), *additional_filters_args))

        if only_last:
            data = self.cursor.fetchone()

            data["clinic"] = self.get_clinic(clinic_id=data["clinic"])
            data["donor"] = self.get_donor(db_id=data["donor"])
            data["status"] = self.get_status(status_id=data["status"])

            return Appointment(data=data) if data is not None else None
        else:
            data = self.cursor.fetchall()
            for i, data_component in enumerate(data, start=0):

                data_component["clinic"] = self.get_clinic(clinic_id=data_component["clinic"])
                data_component["donor"] = self.get_donor(db_id=data_component["donor"])
                data_component["status"] = self.get_status(status_id=data_component["status"])

                data[i] = Appointment(data=data_component)

            return data if data is not None else None

    def get_clinics_by(self, db_id: int = -1, city: int = -1, region: int = -1, street: int = -1, area: int = -1,
                       address: int = -1) -> list:

        query = ('SELECT clinic.* '
                 'FROM '
                 'data_blood.clinic AS clinic, '
                 'data_blood.city AS city, '
                 'data_blood.region AS region, '
                 'data_blood.street AS street, '
                 'data_blood.area AS area, '
                 'data_blood.address AS address'
                 ' WHERE '
                 'clinic."address_ID" = address."ID"'
                 ' AND '
                 'address."area_ID" = area."ID"'
                 ' AND '
                 'address."city_ID" = city."ID"'
                 ' AND '
                 'address."region_ID" = region."ID"'
                 ' AND '
                 'address."street_ID" = street."ID"'
                 ' AND '
                 '(clinic."ID" = %s'
                 ' OR '
                 'city."ID" = %s'
                 ' OR '
                 'region."ID" = %s'
                 ' OR '
                 'street."ID" = %s'
                 ' OR '
                 'area."ID" = %s'
                 ' OR '
                 'clinic."address_ID" = %s)')

        self.cursor.execute(query, (db_id, city, region, street, area, address))

        data = self.cursor.fetchall()

        return data if data is not None else []

    def add_bloods(self):

        query = 'DELETE FROM data_blood.blood_and_components'
        self.cursor.execute(query)

        query = 'INSERT INTO data_blood.blood_and_components ("ID", "blood_and_comp_name") VALUES (%s, %s)'
        self.cursor.executemany(query, cfg.BLOODS)

        self.connection.commit()

    def add_languages(self):

        query = 'DELETE FROM donor.language'
        self.cursor.execute(query)

        query = 'INSERT INTO donor.language ("ID", "lang_name") VALUES (%s, %s)'
        self.cursor.executemany(query, cfg.LANGUAGES)

        self.connection.commit()

    def add_cities(self):

        query = 'DELETE FROM data_blood.city'
        self.cursor.execute(query)

        query = 'INSERT INTO data_blood.city ("ID", "city_name") VALUES (%s, %s)'
        self.cursor.executemany(query, cfg.CITIES)

        self.connection.commit()

    def add_regions(self):

        query = 'DELETE FROM data_blood.region'
        self.cursor.execute(query)

        query = 'INSERT INTO data_blood.region ("ID", "region_name") VALUES (%s, %s)'
        self.cursor.executemany(query, cfg.REGIONS)

        self.connection.commit()

    def add_streets(self):

        query = 'DELETE FROM data_blood.street'
        self.cursor.execute(query)

        query = 'INSERT INTO data_blood.street ("ID", "street_name") VALUES (%s, %s)'
        self.cursor.executemany(query, cfg.STREETS)

        self.connection.commit()

    def add_areas(self):

        query = 'DELETE FROM data_blood.area'
        self.cursor.execute(query)

        query = 'INSERT INTO data_blood.area ("ID", "area_name") VALUES (%s, %s)'
        self.cursor.executemany(query, cfg.AREAS)

        self.connection.commit()

    def add_addresses(self):

        query = 'DELETE FROM data_blood.address'
        self.cursor.execute(query)

        query = ('INSERT INTO data_blood.address ("ID", "region_ID", "city_ID", "area_ID", "street_ID", '
                 '"house_number") VALUES (%s, %s, %s, %s, %s, %s)')
        self.cursor.executemany(query, cfg.ADDRESSES)

        self.connection.commit()

    def add_statuses(self):

        query = 'DELETE FROM data_blood.status_appointment'
        self.cursor.execute(query)

        query = 'INSERT INTO data_blood.status_appointment ("ID", "name_status") VALUES (%s, %s)'
        self.cursor.executemany(query, cfg.STATUSES)

        self.connection.commit()

    def add_genders(self):

        query = 'DELETE FROM donor.gender'
        self.cursor.execute(query)

        query = 'INSERT INTO donor.gender ("ID", "gender_name") VALUES (%s, %s)'
        self.cursor.executemany(query, cfg.GENDERS)

        self.connection.commit()

    def add_clinics(self):

        query = 'DELETE FROM data_blood.clinic'
        self.cursor.execute(query)

        query = ('INSERT INTO data_blood.clinic ("ID", "clinic_name", "address_ID", "working_hours") VALUES (%s, %s, '
                 '%s, %s)')
        self.cursor.executemany(query, cfg.CLINICS)

        self.connection.commit()

    def add_admins(self):

        query = 'DELETE FROM admin.admin'
        self.cursor.execute(query)

        query = ('INSERT INTO admin.admin ("ID", "name_admin", "password", "clinic_ID") VALUES (%s, %s, '
                 '%s, %s)')
        self.cursor.executemany(query, cfg.ADMINS)

        self.connection.commit()

    def add_feedback_request(self, user_id: int | str, note: str) -> None:
        """
        Добавляет запрос на поддержку в базу данных.

        - `user_id` - идентификатор пользователя.
        - `note` - примечание к запросу.
        """
        try:
            query = """INSERT INTO admin.waiting_feed_back ("status_ID", "donor_number_ID", "note")
                        SELECT %s, "ID", %s FROM "number_telephone".donor_number WHERE "donor_ID" = %s"""
            self.cursor.execute(query, (3, note, user_id))
            self.connection.commit()
            print("`add_support_request` sent successfully!")
        except Exception as error:
            print("`add_support_request` ERROR:", error)

    def set_user_language(self, user_id: int, language: str, only_cache: bool = False):

        """
        Устанавливает значение языка в БД и кеше бота чтобы в дальнейшем при запросах языка не обращаться в БД.
        """

        real_language = None

        for language_component in cfg.LANGUAGES:
            if language in language_component:
                real_language = language_component
                break

        if real_language is None:
            return False

        if (not str(user_id) in self.languages_cache) or (self.languages_cache[str(user_id)] != language):

            if not only_cache:
                query = 'UPDATE donor.donor AS donors SET "language_ID" = %s WHERE donors."telegram_ID" = %s'
                self.cursor.execute(query, (real_language[0], user_id))

                self.connection.commit()

            self.languages_cache[str(user_id)] = real_language[1]
            json.dump(self.languages_cache, open("bot/cache/user_languages.json", "w", encoding="UTF-8"))

            return True

    def get_user_language(self, user_id: int | str) -> str:
        return self.languages_cache[str(user_id)] if str(user_id) in self.languages_cache else cfg.DEFAULT_LANGUAGE

    def set_user_notifications(self, user_id: int | str, option: bool):
        if (not str(user_id) in self.notifications_cache) or (self.notifications_cache[str(user_id)] != option):
            self.notifications_cache[str(user_id)] = option
            json.dump(self.notifications_cache, open("bot/cache/user_notifications.json", "w", encoding="UTF-8"))

    def get_user_notifications(self, user_id: int | str) -> bool:
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

        self.add_admins()
        print("Таблица админов заполнена!")
