from src.classes.Datatypes.CRMBaseDataType import CRMBaseDataType


class Area(CRMBaseDataType):
    def set_area_name(self, area_name: str):
        self.data["area_name"] = area_name

    def get_area_name(self) -> str:
        return self.get_from_data(key_name="area_name")
