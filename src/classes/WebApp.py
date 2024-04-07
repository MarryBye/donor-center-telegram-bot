from quart import *

class WebApp(Quart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.config["SECRET_KEY"] = "KluchKotorogoNiktoNeZnaet5"