from src.classes.Datatypes.CRMBaseDataType import CRMBaseDataType


class Telephone(CRMBaseDataType):

    def set_number(self, number: str):
        self.data["number"] = number

    def get_number(self) -> str:
        return self.get_from_data(key_name="number")

