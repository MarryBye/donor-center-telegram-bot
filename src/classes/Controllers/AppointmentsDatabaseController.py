from src.classes.Controllers.DatabaseController import DatabaseController
from src.classes.Datatypes.Appointment import Appointment
from src.classes.Datatypes.Donor import Donor
from src.classes.TerminalColors import TerminalColors

from src.funcs.debug_print import debug_print


class AppointmentsDatabaseController(DatabaseController):

    def get_donor_appointments(self, donor: Donor, need_status: int = None, need_registration_date: str = None,
                               need_appointment_date: str = None, only_last: bool = True) -> Appointment | bool | list:

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
            'appointments.* '
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

        self.cursor.execute(query + additional_filters, (
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



    def delete_donor_appointment(self, donor: Donor, appointment: Appointment):
        pass

    def change_donor_appointment_status(self, appointment_id: int, donor: Donor):
        pass
