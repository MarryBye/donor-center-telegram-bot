from src.classes.DatabaseControllers.DatabaseController import DatabaseController
from src.classes.Datatypes.Donor import Donor
from src.classes.Crypto import CryptoSHA256
from src.classes.TerminalColors import TerminalColors

from src.funcs.debug_print import debug_print


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
                CryptoSHA256.crypt(string=donor.get_password(), salt=donor.get_email()),
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

            query = (
                'DELETE FROM number_telephone.donor_number AS numbers WHERE numbers.number = %s OR numbers."ID" = %s '
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

    def update_donor_field(self, donor: Donor, field_name: str, new_value: int | str):
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

    def update_donor_fields(self, donor: Donor, **fields: dict[str, int | str]):
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
