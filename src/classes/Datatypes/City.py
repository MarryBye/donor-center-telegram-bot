from src.classes.Datatypes.CRMBaseDataType import CRMBaseDataType


class City(CRMBaseDataType):
    def set_city_name(self, city_name: str):
        self.data["city_name"] = city_name

    def get_city_name(self) -> str:
        return self.get_from_data(key_name="city_name")
