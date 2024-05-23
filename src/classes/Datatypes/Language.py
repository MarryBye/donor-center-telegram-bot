from src.classes.Datatypes.CRMBaseDataType import CRMBaseDataType


class Language(CRMBaseDataType):

    def set_lang_name(self, lang_name: str):
        self.data["lang_name"] = lang_name

    def get_lang_name(self) -> str:
        return self.get_from_data(key_name="lang_name")
