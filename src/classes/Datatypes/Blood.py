from src.classes.Datatypes.CRMBaseDataType import CRMBaseDataType


class Blood(CRMBaseDataType):

    def set_blood_and_comp_name(self, blood_and_comp_name: str):
        self.data["blood_and_comp_name"] = blood_and_comp_name

    def get_blood_and_comp_name(self) -> str:
        return self.get_from_data(key_name="blood_and_comp_name")
