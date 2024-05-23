from src.classes.Datatypes.CRMBaseDataType import CRMBaseDataType
from src.classes.Datatypes.Clinic import Clinic
from src.classes.Datatypes.Blood import Blood


class HasBlood(CRMBaseDataType):

    def set_blood(self, blood: Blood):
        self.data["blood"] = blood

    def get_blood(self) -> Blood:
        return self.get_from_data(key_name="blood")

    def set_clinic(self, clinic: Clinic):
        self.data["clinic"] = clinic

    def get_clinic(self) -> Clinic:
        return self.get_from_data(key_name="clinic")

    def set_quantity(self, quantity: int):
        self.data["quantity"] = quantity

    def get_quantity(self) -> int:
        return self.get_from_data(key_name="quantity")