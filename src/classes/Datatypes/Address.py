from src.classes.Datatypes.CRMBaseDataType import CRMBaseDataType
from src.classes.Datatypes.Area import Area
from src.classes.Datatypes.City import City
from src.classes.Datatypes.Street import Street
from src.classes.Datatypes.Region import Region


class Address(CRMBaseDataType):

    def set_area(self, area: Area):
        self.data["area"] = area

    def get_area(self) -> Area:
        return self.get_from_data(key_name="area")

    def set_region(self, region: Region):
        self.data["region"] = region

    def get_region(self) -> Region:
        return self.get_from_data(key_name="region")

    def set_city(self, city: City):
        self.data["city"] = city

    def get_city(self) -> City:
        return self.get_from_data(key_name="city")

    def set_street(self, street: Street):
        self.data["street"] = street

    def get_street(self) -> Street:
        return self.get_from_data(key_name="street")

    def set_house_number(self, house_number: int):
        self.data["house_number"] = house_number

    def get_house_number(self) -> int:
        return self.get_from_data(key_name="house_number")
