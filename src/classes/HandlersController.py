from src.classes.Singleton import Singleton


class HandlersController(metaclass=Singleton):
    def __init__(self):
        self.__routers = []

    def add_router(self, rt):
        self.__routers.append(rt)

    def get_routers(self):
        return self.__routers
