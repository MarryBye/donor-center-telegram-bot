class Singleton(type):
    _insts = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._insts:
            inst = super().__call__(*args, **kwargs)
            cls._insts[cls] = inst
        return cls._insts[cls]