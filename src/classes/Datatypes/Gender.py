from src.classes.Datatypes.CRMBaseDataType import CRMBaseDataType


class Gender(CRMBaseDataType):

    def set_gender_name(self, gender_name: str):
        self.data["gender_name"] = gender_name

    def get_gender_name(self) -> str:
        return self.get_from_data(key_name="gender_name")
