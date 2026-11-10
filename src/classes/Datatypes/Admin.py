from src.classes.Datatypes.Clinic import Clinic
from src.classes.Datatypes.CRMBaseDataType import CRMBaseDataType


class Admin(CRMBaseDataType):
    def get_clinic(self) -> Clinic:
        return self.get_from_data(key_name="clinic")
