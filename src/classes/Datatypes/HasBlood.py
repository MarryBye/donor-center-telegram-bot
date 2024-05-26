import src.classes.Datatypes as Datatypes
import src.classes.Controllers.DatabaseController as Db

from src.classes.Datatypes.CRMBaseDataType import CRMBaseDataType


class HasBlood(CRMBaseDataType):

    def set_blood(self, blood: Datatypes.Blood.Blood):
        self.data["blood"] = blood

    def get_blood(self) -> Datatypes.Blood.Blood:
        return self.get_from_data(key_name="blood")

    def set_clinic(self, clinic: Datatypes.Clinic.Clinic):
        self.data["clinic"] = clinic

    def get_clinic(self) -> Datatypes.Clinic.Clinic:
        return Db.DatabaseController().get_clinic(db_id=self.get_from_data(key_name="clinic"))

    def set_quantity(self, quantity: int):
        self.data["quantity"] = quantity

    def get_quantity(self) -> int:
        return self.get_from_data(key_name="quantity")
