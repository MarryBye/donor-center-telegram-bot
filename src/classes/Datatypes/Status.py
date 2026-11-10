from src.classes.Datatypes.CRMBaseDataType import CRMBaseDataType


class Status(CRMBaseDataType):
    def set_name_status(self, name_status: str):
        self.data["name_status"] = name_status

    def get_name_status(self) -> str:
        return self.get_from_data(key_name="name_status")
