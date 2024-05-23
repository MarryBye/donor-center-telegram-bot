from src.classes.Datatypes.CRMBaseDataType import CRMBaseDataType


class Region(CRMBaseDataType):

    def set_region_name(self, region_name: str):
        self.data["region_name"] = region_name

    def get_region_name(self) -> str:
        return self.get_from_data(key_name="region_name")
