from src.classes.Datatypes.CRMBaseDataType import CRMBaseDataType
from src.classes.Datatypes.Donor import Donor
from src.classes.Datatypes.Clinic import Clinic


class Review(CRMBaseDataType):

    def set_donor(self, donor: Donor):
        self.data["donor"] = donor

    def get_donor(self) -> Donor:
        return self.get_from_data(key_name="donor")

    def set_clinic(self, clinic: Clinic):
        self.data["clinic"] = clinic

    def get_clinic(self) -> Clinic:
        return self.get_from_data(key_name="clinic")

    def set_rating(self, rating: int):
        self.data["rating"] = rating

    def get_rating(self) -> int:
        return self.get_from_data(key_name="rating")

    def set_comment(self, comment: str):
        self.data["comment"] = comment

    def get_comment(self) -> str:
        return self.get_from_data(key_name="comment")

    def set_date_added(self, date_added: str):
        self.data["date_added"] = date_added

    def get_date_added(self) -> str:
        return self.get_from_data(key_name="date_added")
