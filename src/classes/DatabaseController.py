import psycopg2
import psycopg2 as psql
import psycopg2.extras as psql_extra
import config as cfg
import json

from typing import Union

from src.classes.Singleton import Singleton
from src.classes.Donor import Donor
from src.classes.Appointment import Appointment
from src.classes.Crypto import Crypto
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

    def get_cities(self):

        query = 'SELECT * FROM data_blood.city'
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        return data if data is not None else []

    def get_regions(self):

        query = 'SELECT * FROM data_blood.region'
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        return data if data is not None else []

    def get_streets(self):
        query = 'SELECT * FROM data_blood.street'
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        return data if data is not None else []

    def get_areas(self):

        query = 'SELECT * FROM data_blood.area'
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        return data if data is not None else []

    def get_addresses(self):

        query = 'SELECT * FROM data_blood.address'
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        return data if data is not None else []

    def get_clinics(self):

        query = 'SELECT * FROM data_blood.clinic'
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        return data if data is not None else []

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

    def add_feedback_request(self, user_id: Union[int, str], note: str) -> None:
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

        self.add_admins()
        print("Таблица админов заполнена!")


class DonorsDatabaseController(DatabaseController):

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
        self.cursor.execute(query, (db_id, telegram_id, number, email))

        data = self.cursor.fetchone()

        return Donor(data=data) if data is not None else Donor()

    def get_donors(self) -> list[Donor]:

        """
        Получить список всех доноров существующих в БД в виде объектов ``Donor``.
        """

        query = ('SELECT donors.*, numbers."ID" AS number_ID, numbers.number AS number FROM donor.donor as donors, '
                 'number_telephone.donor_number AS numbers WHERE donors."ID" = numbers."donor_ID"')
        self.cursor.execute(query)

        data = self.cursor.fetchall()

        for i, donor_data in enumerate(data, start=0):
            data[i] = Donor(data=donor_data)

        return data

    def register_donor(self, donor: Donor) -> bool:

        """
        Регистрация донора и добавление его в БД если его в ней нет. В качестве аргумента принимает:
        - ``donor`` - объект ``Donor`` с информацией про нового донора.\n
        В случае успешного выполнения будет возвращено значение ``True``, в ином случае ``False``.
        """

        donor.set_id(db_id=self.get_next_row_id(table="donor.donor"))
        donor.set_number_id(number_id=self.get_next_row_id(table="number_telephone.donor_number"))

        try:

            query = ('INSERT INTO donor.donor ("ID", "name_donor", "surname_donor", "date_of_birth", "gender_ID", '
                     '"email", "telegram_ID", "password", "language_ID") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
            self.cursor.execute(query, (
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

            debug_print("Donor has inserted into database!")

            query = 'INSERT INTO number_telephone.donor_number ("ID", "donor_ID", "number") VALUES (%s, %s, %s)'
            self.cursor.execute(query, (
                donor.get_number_id(),
                donor.get_id(),
                donor.get_number()
            )
                                )

            self.connection.commit()

            debug_print("Donor telephone has inserted into database!")

            debug_print("Donor has successfully registered!")

            return True

        except Exception as e:

            debug_print(f"Donor can`t be registered! Error: \n{e}", color=TerminalColors.FAIL)

            return False

    def delete_donor(self, donor: Donor):

        """
        Удалить донора из таблицы доноров, а также его номер телефона, который к нему привязан.Принимает следующие
        аргументы:
        - ``donor`` - принимает объект ``Donor`` с данными про донора.\n
        Метод возвращает ``False`` если донора удалить не получилось.
        """

        try:

            query = ('DELETE FROM donor.donor as donors WHERE donors."ID" = %s OR donors."telegram_ID" = %s OR '
                     'donors.email = %s')
            self.cursor.execute(query, (donor.get_id(), donor.get_telegram(), donor.get_email()))

            debug_print("Donor has successfully deleted!")

            query = ('DELETE FROM number_telephone.donor_number AS numbers WHERE numbers.number = %s OR numbers."ID" = %s '
                     'OR numbers."donor_ID" = %s')
            self.cursor.execute(query, (donor.get_number(), donor.get_number_id(), donor.get_id()))

            debug_print("Donor telephone has successfully deleted!")

            query = 'DELETE FROM data_blood.appointment AS appointments WHERE appointments."donor_number_ID" = %s'
            self.cursor.execute(query, (donor.get_id(),))

            debug_print("Donor appointments has successfully deleted!")

            self.connection.commit()

            return True

        except Exception as e:

            debug_print(f"Donor can`t be deleted! Error: \n{e}", color=TerminalColors.FAIL)

            return False

    def update_donor_number(self, donor_id, new_phone_number):

        try:

            query = 'UPDATE number_telephone.donor_number SET number = %s WHERE "donor_ID" = %s'
            self.cursor.execute(query, (new_phone_number, donor_id))

            self.connection.commit()

            debug_print("Donor number has successfully updated!")

            return True

        except Exception as e:

            debug_print(f"Donor number can`t be updated! Error: \n{e}", color=TerminalColors.FAIL)

            return False

    def update_donor_field(self, donor: Donor, field_name: str, new_value: Union[int, str]):
        """Меняет одно значение информации о пользователе

        - `donor` - объект `Donor` с информацией про нового донора.
        - `field_name` - название колонки информации. Их список: `name_donor`, `email`, `password`, `date_of_birth`, `gender_ID`, `phone_number`.
        - `new_value` - новое значение колонки.
        """

        try:
            if field_name in ['name_donor', 'email', 'password', 'date_of_birth', 'gender_ID', 'phone_number']:
                user_id = donor.get_id()

                if field_name == "phone_number":
                    self.update_donor_number(user_id, new_value)

                with self.connection.cursor() as cur:
                    cur.execute(
                        f'''UPDATE donor.donor SET "{field_name}" = %s WHERE "ID" = %s;''',
                        (new_value, user_id),
                    )
                self.connection.commit()

                print(f"{field_name} донора успешно обновлено.")
            else:
                print(
                    "Такого названия колонки нет в списке доступных:\n['name_donor', 'email', 'password', 'date_of_birth', 'gender_ID', 'phone_number']")
        except Exception as e:
            print(f"Ошибка при обновлении {field_name} донора: {e}")

    def update_donor_fields(self, donor: Donor, **fields: dict[str, Union[int, str]]):
        """Меняет несколько значений информации о пользователе

        - `donor` - объект `Donor` с информацией про нового донора.
        fields:
        - `name_donor`: Новое имя донора.
        - `email`: Новый адрес электронной почты донора.
        - `password`: Новый пароль донора.
        - `date_of_birth`: Новая дата рождения донора (в формате 'YYYY-MM-DD').
        - `gender_ID`: Новый идентификатор гендера донора.
        - `phone_number`: Новый номер телефона донора.
        Пример:
            update_donor_fields(donor, name_donor="NewName", email="new.mail@gmail.com")
        """

        try:
            user_id = donor.get_id()
            fields = fields.get('fields')

            set_fields = ", ".join([f'"{field}" = %s' for field in fields.keys()])

            if "phone_number" in fields:
                self.update_donor_number(user_id, fields.pop("phone_number"))

            with self.connection.cursor() as cur:
                cur.execute(
                    f"""UPDATE donor.donor SET {set_fields} WHERE "ID" = %s""",
                    list(fields.values()) + [user_id],
                )
            self.connection.commit()

            print("Данные донора успешно обновлены.")
        except Exception as e:
            print(f"Ошибка при обновлении данных донора: {e}")


class AppointmentsDatabaseController(DatabaseController):

    def get_donor_appointments(self, donor: Donor, need_status: int = None, need_registration_date: str = None,
                               need_appointment_date: str = None, only_last: bool = True) -> Union[Appointment, bool, list]:

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
                 'numbers.number = %s OR donors.email = %s)' + additional_filters)
        self.cursor.execute(query, (
            donor.get_id(), donor.get_telegram(), donor.get_number(), donor.get_email(), *additional_filters_args))

        if only_last:
            data = self.cursor.fetchone()
            return Appointment(data=data) if data is not None else Appointment()
        else:
            data = self.cursor.fetchall()
            for i, data_component in enumerate(data, start=0):
                data[i] = Appointment(data=data_component)
            return data if data is not None else []

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
        self.cursor.execute(query, (donor.get_id(), donor.get_telegram(), donor.get_number(), donor.get_email()))

        data = self.cursor.fetchone()
        is_registered = data is not None

        return is_registered

    def register_donor_appointment(self, appointment: Appointment, donor: Donor):

        """
        Зарегистрировать донора на прием. Принимает следующие аргументы:
        - ``appointment`` - принимает объект ``Appointment`` с данными про новый прием;
        - ``donor`` - принимает объект ``Donor`` с данными про донора.\n
        Метод возвращает ``False`` если донор уже зарегистрирован на прием или нет данных о доноре.
        """

        appointment.set_id(db_id=self.get_next_row_id(table="data_blood.appointment"))
        appointment.set_donor_number_id(donor_number_id=donor.get_number_id())
        appointment.set_status_id(status_id=3)

        try:

            query = ('INSERT INTO data_blood.appointment ("ID", "clinic_ID", "donor_number_ID", "status_ID", "registration_date", "appointment_date", "analysis_file_path") VALUES (%s, %s, %s, %s, %s, %s, %s)')
            self.cursor.execute(query, (
                appointment.get_id(),
                appointment.get_clinic_id(),
                appointment.get_donor_number_id(),
                appointment.get_status_id(),
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

    def delete_donor_appointment(self, donor: Donor, appointment: Appointment):
        pass

    def change_donor_appointment_status(self, appointment_id: int, donor: Donor):
        pass