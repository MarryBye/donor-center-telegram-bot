from src.classes.Singleton import Singleton

class KB:
    register = "RegistrationKB"
    main = "MainKB"
    donation = "DonationKB"
    feedback = "FeedbackKB"
    languages = "LanguagesKB"
    settings = "SettingsKB"

class KeyboardsController(metaclass=Singleton):
    def __init__(self):
        self.__keyboards = {}
        
    def add_keyboard(self, name, kb):
        self.__keyboards[name] = kb
        
    def get_keyboard(self, name):
        return self.__keyboards[name]