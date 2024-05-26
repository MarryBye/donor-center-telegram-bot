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
from src.classes.Datatypes.Donor import Donor, Telephone
from src.classes.Datatypes.Appointment import Appointment
from src.classes.Datatypes.Review import Review
from src.classes.Datatypes.HasBlood import HasBlood
from src.classes.Datatypes.Gender import Gender
from src.classes.Datatypes.Language import Language

from src.classes.Crypto import CryptoSHA256
from src.classes.TerminalColors import TerminalColors

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

    def add_cities(self):

        query = 'DELETE FROM data_blood.city'
        self.cursor.execute(query)

        query = 'INSERT INTO data_blood.city ("ID", "city_name") VALUES (%s, %s)'
        self.cursor.executemany(query, cfg.CITIES)

        self.connection.commit()

    def get_city(self, db_id: int | str) -> City | None:

        query = 'SELECT * FROM data_blood.city AS city WHERE city."ID" = %s'
        self.cursor.execute(query, (db_id,))
        data = self.cursor.fetchone()

        return City(data=data) if data is not None else None

    def get_cities(self, n: int = -1) -> list[City] | None:

        query = 'SELECT * FROM data_blood.city'
        self.cursor.execute(query)
        data = self.cursor.fetchmany(n)

        for i, data_component in enumerate(data, start=0):
            data[i] = City(data=data_component)

        return data if data is not None else None

    def add_regions(self):

        query = 'DELETE FROM data_blood.region'
        self.cursor.execute(query)

        query = 'INSERT INTO data_blood.region ("ID", "region_name") VALUES (%s, %s)'
        self.cursor.executemany(query, cfg.REGIONS)

        self.connection.commit()

    def get_region(self, db_id: int | str) -> Region | None:

        query = 'SELECT * FROM data_blood.region AS region WHERE region."ID" = %s'
        self.cursor.execute(query, (db_id,))
        data = self.cursor.fetchone()

        return Region(data=data) if data is not None else None

    def get_regions(self, n: int = -1) -> list[Region] | None:

        query = 'SELECT * FROM data_blood.region'
        self.cursor.execute(query)
        data = self.cursor.fetchmany(n)

        for i, data_component in enumerate(data, start=0):
            data[i] = Region(data=data_component)

        return data if data is not None else None

    def add_streets(self):

        query = 'DELETE FROM data_blood.street'
        self.cursor.execute(query)

        query = 'INSERT INTO data_blood.street ("ID", "street_name") VALUES (%s, %s)'
        self.cursor.executemany(query, cfg.STREETS)

        self.connection.commit()

    def get_street(self, db_id: int | str) -> Street | None:
        query = 'SELECT * FROM data_blood.street AS street WHERE street."ID" = %s'
        self.cursor.execute(query, (db_id,))
        data = self.cursor.fetchone()

        return Street(data=data) if data is not None else None

    def get_streets(self, n: int = -1) -> list[Street] | None:

        query = 'SELECT * FROM data_blood.street'
        self.cursor.execute(query)
        data = self.cursor.fetchmany(n)

        for i, data_component in enumerate(data, start=0):
            data[i] = City(data=data_component)

        return data if data is not None else None

    def add_areas(self):

        query = 'DELETE FROM data_blood.area'
        self.cursor.execute(query)

        query = 'INSERT INTO data_blood.area ("ID", "area_name") VALUES (%s, %s)'
        self.cursor.executemany(query, cfg.AREAS)

        self.connection.commit()

    def get_area(self, db_id: int | str) -> Area | None:

        query = 'SELECT * FROM data_blood.area AS area WHERE area."ID" = %s'
        self.cursor.execute(query, (db_id,))
        data = self.cursor.fetchone()

        return Area(data=data) if data is not None else None

    def get_areas(self, n: int = -1) -> list[Area] | None:

        query = 'SELECT * FROM data_blood.area'
        self.cursor.execute(query)
        data = self.cursor.fetchmany(n)

        for i, data_component in enumerate(data, start=0):
            data[i] = City(data=data_component)

        return data if data is not None else None

    def add_addresses(self):

        query = 'DELETE FROM data_blood.address'
        self.cursor.execute(query)

        query = ('INSERT INTO data_blood.address ("ID", "region_ID", "city_ID", "area_ID", "street_ID", '
                 '"house_number") VALUES (%s, %s, %s, %s, %s, %s)')
        self.cursor.executemany(query, cfg.ADDRESSES)

        self.connection.commit()

    def get_address(self, db_id: int | str) -> Address | None:

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

        self.cursor.execute(query, (db_id,))
        data = self.cursor.fetchone()

        data["area"] = self.get_area(db_id=data["area"])
        data["city"] = self.get_city(db_id=data["city"])
        data["region"] = self.get_region(db_id=data["region"])
        data["street"] = self.get_street(db_id=data["street"])

        return Address(data=data) if data is not None else None

    def get_addresses(self, n: int = -1) -> list[Address] | None:

        query = (
            'SELECT '
            'address."ID", '
            'address."area_ID" AS area, '
            'address."city_ID" AS city, '
            'address."region_ID" AS region, '
            'address."street_ID" AS street, '
            'address."house_number" AS house '
            'FROM data_blood.address AS address '
        )
        self.cursor.execute(query)
        data = self.cursor.fetchmany(n)

        for i, data_component in enumerate(data, start=0):
            data_component["area"] = self.get_area(db_id=data_component["area"])
            data_component["city"] = self.get_city(db_id=data_component["city"])
            data_component["region"] = self.get_region(db_id=data_component["region"])
            data_component["street"] = self.get_street(db_id=data_component["street"])

            data[i] = Address(data=data_component)

        return data if data is not None else None

    def add_clinics(self):

        query = 'DELETE FROM data_blood.clinic'
        self.cursor.execute(query)

        query = 'DELETE FROM data_blood.clinic_has_blood_and_comp'
        self.cursor.execute(query)

        query = ('INSERT INTO data_blood.clinic ("ID", "clinic_name", "address_ID", "working_hours") VALUES (%s, %s, '
                 '%s, %s)')
        self.cursor.executemany(query, cfg.CLINICS)

        query = (
            'INSERT INTO data_blood.clinic_has_blood_and_comp ("blood_and_comp_ID", "clinic_ID", "kol") VALUES (%s, %s, '
            '%s)')

        query_args = []

        for clinic in cfg.CLINICS:
            for blood in cfg.BLOODS:
                query_args.append((blood[0], clinic[0], 0))

        self.cursor.executemany(query, query_args)

        self.connection.commit()

    def get_clinic(self, db_id: int | str = -1, address_id: int | str = -1, city_id: int | str = -1, region_id: int | str = -1) -> Clinic | None:

        query = (
            'SELECT '
            'clinic."ID", '
            'clinic."clinic_name", '
            'clinic."address_ID" AS address, '
            'clinic."working_hours" '
            'FROM data_blood.clinic AS clinic, '
            'data_blood."address" AS address '
            'WHERE clinic."address_ID" = address."ID" AND '
            '(clinic."ID" = %s OR clinic."address_ID" = %s OR address."city_ID" = %s OR address."region_ID" = %s)'
        )

        self.cursor.execute(query, (db_id, address_id, city_id, region_id))
        data = self.cursor.fetchone()

        data["address"] = self.get_address(db_id=data["address"])
        data["has_blood"] = self.get_has_blood(clinic_id=data["ID"])

        return Clinic(data=data) if data is not None else None

    def get_clinics(self, n: int = -1) -> list[Clinic] | None:

        query = (
            'SELECT '
            'clinic."ID", '
            'clinic."clinic_name", '
            'clinic."address_ID" AS address, '
            'clinic."working_hours" '
            'FROM data_blood.clinic AS clinic '
        )
        self.cursor.execute(query)
        data = self.cursor.fetchmany(n)

        for i, data_component in enumerate(data, start=0):
            data_component["address"] = self.get_address(db_id=data_component["address"])
            data_component["has_blood"] = self.get_has_blood(clinic_id=data_component["ID"])

            data[i] = Clinic(data=data_component)

        return data if data is not None else None

    def add_bloods(self):

        query = 'DELETE FROM data_blood.blood_and_components'
        self.cursor.execute(query)

        query = 'INSERT INTO data_blood.blood_and_components ("ID", "blood_and_comp_name") VALUES (%s, %s)'
        self.cursor.executemany(query, cfg.BLOODS)

        self.connection.commit()

    def get_blood(self, db_id: int | str) -> Blood | None:

        query = 'SELECT blood.* FROM data_blood.blood_and_components AS blood WHERE blood."ID" = %s'

        self.cursor.execute(query, (db_id,))
        data = self.cursor.fetchone()

        return Blood(data=data) if data is not None else None

    def get_bloods(self, n: int = -1) -> list[Blood] | None:

        query = 'SELECT * FROM data_blood.blood_and_components'
        self.cursor.execute(query)
        data = self.cursor.fetchmany(n)

        for i, data_component in enumerate(data, start=0):
            data[i] = Blood(data=data_component)

        return data if data is not None else None

    def add_statuses(self):

        query = 'DELETE FROM data_blood.status_appointment'
        self.cursor.execute(query)

        query = 'INSERT INTO data_blood.status_appointment ("ID", "name_status") VALUES (%s, %s)'
        self.cursor.executemany(query, cfg.STATUSES)

        self.connection.commit()

    def get_status(self, db_id: int | str) -> Status | None:

        query = 'SELECT status.* FROM data_blood.status_appointment AS status WHERE status."ID" = %s'

        self.cursor.execute(query, (db_id,))
        data = self.cursor.fetchone()

        return Status(data=data) if data is not None else None

    def get_statuses(self, n: int = -1) -> list[Status] | None:

        query = 'SELECT * FROM data_blood.status_appointment'
        self.cursor.execute(query)
        data = self.cursor.fetchmany(n)

        for i, data_component in enumerate(data, start=0):
            data[i] = Status(data=data_component)

        return data if data is not None else None

    def get_review(self, db_id: int | str = -1, donor_id: int | str = -1, clinic_id: int | str = -1) -> Review | None:

        query = (
            'SELECT '
            'review."ID",'
            'review."donor_ID" AS donor,'
            'review."clinic_ID" AS clinic,'
            'review."rating",'
            'review."comment",'
            'review.date_added '
            'FROM data_blood."reviews" AS review '
            'WHERE (review."ID" = %s OR review."donor_ID" = %s OR review."clinic_ID" = %s)'
        )

        self.cursor.execute(query, (db_id, donor_id, clinic_id))

        data = self.cursor.fetchone()

        data["donor"] = self.get_donor(db_id=data["donor"])
        data["clinic"] = self.get_clinic(db_id=data["clinic"])

        return Review(data=data) if data is not None else None

    def get_reviews(self, n: int = -1) -> list[Review] | None:

        query = (
            'SELECT '
            'review."ID",'
            'review."donor_ID" AS donor,'
            'review."clinic_ID" AS clinic,'
            'review."rating",'
            'review."comment",'
            'review.date_added '
            'FROM data_blood."reviews" AS review '
        )
        self.cursor.execute(query)
        data = self.cursor.fetchmany(n)

        for i, data_component in enumerate(data, start=0):
            data_component["donor"] = self.get_donor(db_id=data_component["donor"])
            data_component["clinic"] = self.get_clinic(db_id=data_component["clinic"])

            data[i] = Review(data=data_component)

        return data if data is not None else None

    def add_genders(self):

        query = 'DELETE FROM donor.gender'
        self.cursor.execute(query)

        query = 'INSERT INTO donor.gender ("ID", "gender_name") VALUES (%s, %s)'
        self.cursor.executemany(query, cfg.GENDERS)

        self.connection.commit()

    def get_gender(self, db_id: int | str) -> Gender | None:

        query = 'SELECT * FROM donor."gender" AS gender WHERE gender."ID" = %s'
        self.cursor.execute(query, (db_id,))
        data = self.cursor.fetchone()

        return Gender(data=data) if data is not None else None

    def get_genders(self, n: int = -1) -> list[Gender] | None:

        query = 'SELECT * FROM donor."gender"'
        self.cursor.execute(query)
        data = self.cursor.fetchmany(n)

        for i, data_component in enumerate(data, start=0):
            data[i] = Gender(data=data_component)

        return data if data is not None else None

    def add_languages(self):

        query = 'DELETE FROM donor.language'
        self.cursor.execute(query)

        query = 'INSERT INTO donor.language ("ID", "lang_name") VALUES (%s, %s)'
        self.cursor.executemany(query, cfg.LANGUAGES)

        self.connection.commit()

    def get_language(self, db_id: int | str) -> Language | None:

        query = 'SELECT * FROM donor."language" AS language WHERE language."ID" = %s'
        self.cursor.execute(query, (db_id,))
        data = self.cursor.fetchone()

        return Language(data=data) if data is not None else None

    def get_languages(self, n: int = -1) -> list[Language] | None:

        query = 'SELECT * FROM donor."language"'
        self.cursor.execute(query)
        data = self.cursor.fetchmany(n)

        for i, data_component in enumerate(data, start=0):
            data[i] = Language(data=data_component)

        return data if data is not None else None

    def get_telephone(self, db_id: int | str = -1, donor_id: int | str = -1) -> Telephone | None:

        query = (
            'SELECT '
            'number."ID",'
            'number."donor_ID" AS donor, '
            'number."number" '
            'FROM number_telephone."donor_number" AS number,'
            'donor.donor AS donor '
            'WHERE number."donor_ID" = donor."ID" AND '
            '(number."ID" = %s OR number."donor_ID" = %s)'
        )
        self.cursor.execute(query, (db_id, donor_id))
        data = self.cursor.fetchone()

        return Telephone(data=data) if data is not None else None

    def get_telephones(self, n: int = -1) -> list[Telephone] | None:

        query = (
            'SELECT '
            'number."ID",'
            'number."donor_ID" AS donor, '
            'number."number" '
            'FROM number_telephone."donor_number" AS number'
        )
        self.cursor.execute(query)
        data = self.cursor.fetchmany(n)

        for i, data_component in enumerate(data, start=0):
            data[i] = Telephone(data=data_component)

        return data if data is not None else None

    def get_has_blood(self, blood_id: int | str = -1, clinic_id: int | str = -1) -> list[HasBlood] | None:

        query = (
            'SELECT '
            'has_blood."blood_and_comp_ID" AS blood,'
            'has_blood."clinic_ID" AS clinic,'
            'has_blood."kol" AS quantity '
            'FROM data_blood.clinic_has_blood_and_comp AS has_blood '
            'WHERE (has_blood."blood_and_comp_ID" = %s OR has_blood."clinic_ID" = %s)'
        )
        self.cursor.execute(query, (blood_id, clinic_id))

        data = self.cursor.fetchall()

        for i, data_component in enumerate(data, start=0):
            data_component["blood"] = self.get_blood(db_id=data_component["blood"])

            data[i] = HasBlood(data=data_component)

        return data if data is not None else None

    def add_donor(self, donor: Donor) -> bool:

        """
        Регистрация донора и добавление его в БД если его в ней нет. В качестве аргумента принимает:
        - ``donor`` - объект ``Donor`` с информацией про нового донора.\n
        В случае успешного выполнения будет возвращено значение ``True``, в ином случае ``False``.
        """

        new_donor_id = self.get_next_row_id(table="donor.donor")
        new_telephone_id = self.get_next_row_id(table="number_telephone.donor_number")

        try:

            query = (
                'INSERT INTO '
                'donor.donor ("ID", "name_donor", "surname_donor", "date_of_birth", "gender_ID", "email", "telegram_ID", "password", "language_ID") '
                'VALUES '
                '(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            )
            self.cursor.execute(query, (
                new_donor_id,
                donor.get_name(),
                donor.get_surname(),
                donor.get_birthdate(),
                donor.get_gender().get_id(),
                donor.get_email(),
                donor.get_telegram_id(),
                CryptoSHA256.crypt(string=donor.get_password(), salt=donor.get_email()),
                donor.get_language().get_id()
            )
                                )

            debug_print("Donor has inserted into database!")

            query = (
                'INSERT INTO '
                'number_telephone.donor_number ("ID", "donor_ID", "number") '
                'VALUES '
                '(%s, %s, %s)'
            )
            self.cursor.execute(query, (
                new_telephone_id,
                new_donor_id,
                donor.get_telephone().get_number()
            )
                                )

            self.connection.commit()

            debug_print("Donor telephone has inserted into database!")

            debug_print("Donor has successfully registered!")

            return True

        except Exception as e:

            debug_print(f"Donor can`t be registered! Error: \n{e}", color=TerminalColors.FAIL)

            return False

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

        if data is not None:
            data["telephone"] = self.get_telephone(db_id=data["telephone"])
            data["gender"] = self.get_gender(db_id=data["gender"])
            data["language"] = self.get_language(db_id=data["language"])

            return Donor(data=data)

        return None

    def get_donors(self, n: int = -1) -> list[Donor] | None:

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
        )
        self.cursor.execute(query)
        data = self.cursor.fetchmany(n)

        for i, data_component in enumerate(data, start=0):
            data["telephone"] = self.get_telephone(db_id=data["telephone"])
            data["gender"] = self.get_gender(db_id=data["gender"])
            data["language"] = self.get_language(db_id=data["language"])

            data[i] = Donor(data=data_component)

        return data if data is not None else None

    def register_appointment(self, appointment: Appointment, donor: Donor):

        """
        Зарегистрировать донора на прием. Принимает следующие аргументы:
        - ``appointment`` - принимает объект ``Appointment`` с данными про новый прием;
        - ``donor`` - принимает объект ``Donor`` с данными про донора.\n
        Метод возвращает ``False`` если донор уже зарегистрирован на прием или нет данных о доноре.
        """

        new_appointment_id = self.get_next_row_id(table="data_blood.appointment")
        donor_number = donor.get_telephone().get_id()
        new_appointment_status = appointment.get_status().get_id()
        new_appointment_clinic = appointment.get_clinic().get_id()

        try:

            query = (
                'INSERT INTO data_blood.appointment ("ID", "clinic_ID", "donor_number_ID", "status_ID", "registration_date", "appointment_date", "analysis_file_path") VALUES (%s, %s, %s, %s, %s, %s, %s)')
            self.cursor.execute(query, (
                appointment.get_id(),
                new_appointment_clinic,
                donor_number,
                new_appointment_status,
                appointment.get_registration_date(),
                appointment.get_appointment_date(),
                appointment.get_analysis_file_path()
            )
                                )

            self.connection.commit()

            debug_print("Donor appointment has successfully registered!")

            return True

        except Exception as e:

            debug_print(f"Donor appointment can`t be registered! Error: \n{e}", color=TerminalColors.FAIL)

            return False

    def get_appointment(self, donor: Donor, only_last: bool = True, n: int = -1) -> Appointment | list[Appointment] | None:

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
        self.cursor.execute(query, (
        donor.get_id(), donor.get_telegram_id(), donor.get_telephone().get_number(), donor.get_email()))

        if only_last:
            data = self.cursor.fetchone()

            if data is not None:
                data["clinic"] = self.get_clinic(db_id=data["clinic"])
                data["donor"] = self.get_donor(db_id=data["donor"])
                data["status"] = self.get_status(db_id=data["status"])

                return Appointment(data=data)

        else:
            data = self.cursor.fetchmany(n)

            if data is not None:

                for i, data_component in enumerate(data, start=0):
                    data_component["clinic"] = self.get_clinic(db_id=data_component["clinic"])
                    data_component["donor"] = self.get_donor(db_id=data_component["donor"])
                    data_component["status"] = self.get_status(db_id=data_component["status"])

                    data[i] = Appointment(data=data_component)

                return data

        return None

    def get_appointments(self, n: int = -1) -> list[Appointment] | None:

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
        )
        self.cursor.execute(query)

        data = self.cursor.fetchmany(n)

        for i, data_component in enumerate(data, start=0):
            data_component["clinic"] = self.get_clinic(db_id=data_component["clinic"])
            data_component["donor"] = self.get_donor(db_id=data_component["donor"])
            data_component["status"] = self.get_status(db_id=data_component["status"])

            data[i] = Appointment(data=data_component)

        return data if data is not None else None

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
