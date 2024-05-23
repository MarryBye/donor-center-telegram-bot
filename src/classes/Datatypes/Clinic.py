from src.classes.Datatypes.CRMBaseDataType import CRMBaseDataType
from src.classes.Datatypes.Address import Address


class Clinic(CRMBaseDataType):

    def set_clinic_name(self, clinic_name: str):
        self.data["clinic_name"] = clinic_name

    def get_clinic_name(self) -> str:
        return self.get_from_data(key_name="clinic_name")

    def set_address(self, address: Address):
        self.data["address"] = address

    def get_address(self) -> Address:
        return self.get_from_data(key_name="address")

    def set_working_hours(self, working_hours: str):
        self.data["working_hours"] = working_hours

    def get_working_hours(self) -> str:
        return self.get_from_data(key_name="working_hours")
