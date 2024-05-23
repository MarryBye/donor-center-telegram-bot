from src.classes.Datatypes.CRMBaseDataType import CRMBaseDataType


class Street(CRMBaseDataType):

    def set_street_name(self, street_name: str):
        self.data["street_name"] = street_name

    def get_street_name(self) -> str:
        return self.get_from_data(key_name="street_name")
