from psycopg2 import sql

from src.classes.Controllers.DatabaseController import DatabaseController


class BloodController(DatabaseController):
    """
    Класс для взаимодействия с запасами крови
    """

    def get(self, group: str = None, rh: str = None, output_type: str = "list"):
        """
        Показывает запасы крови по фильтрам.

        - `group` - The blood group filter (e.g., 'A', 'B', 'AB', 'O').
        - `rh` - The RH factor filter (e.g., '+', '-').
        - `output_type` - формат получаемой информации: 'list' или 'dict'.
                - `list` - просто список количества для каждой групы крови.
                - `dict` - словарь с названием и количеством.

        Возможные ошибки:
        ValueError: Если output_type не 'list' или 'dict'.
        """
        try:
            conditions = []
            params = []

            if group:
                conditions.append("bc.blood_and_comp_name LIKE %s")
                params.append(f"%{group}%")
            if rh:
                conditions.append("bc.blood_and_comp_name LIKE %s")
                params.append(f"%{rh}%")

            where_clause = " AND ".join(conditions) if conditions else "1=1"
            query = sql.SQL(
                f"""SELECT bc.blood_and_comp_name, chc.kol
                    FROM data_blood.clinic_has_blood_and_comp chc
                    JOIN data_blood.blood_and_components bc
                    ON chc."blood_and_comp_ID" = bc."ID"
                    WHERE {where_clause}"""
            )
            self.cursor.execute(query, params)

            results = self.cursor.fetchall()

            if group and rh:
                if not results:
                    return None

                return results[0]["kol"]
            elif output_type == "list":
                return [result["kol"] for result in results]
            elif output_type == "dict":
                return {result["blood_and_comp_name"]: result["kol"] for result in results}
            else:
                raise ValueError("Invalid output_type. Expected 'list' or 'dict'.")
        except Exception as error:
            print(f"Error getting blood levels: {error}")
            self.connection.rollback()
            return None
