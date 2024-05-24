from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.Datatypes.Donor import Donor
from src.classes.Crypto import CryptoSHA256
from src.classes.TerminalColors import TerminalColors

from src.funcs.debug_print import debug_print


class DonorsDatabaseController(DatabaseController):



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
