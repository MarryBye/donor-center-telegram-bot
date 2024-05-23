from hashlib import sha256
from src.classes.Singleton import Singleton


class CryptoRSA(metaclass=Singleton):
    """
    Класс для шифрования строк (паролей, например) при помощи алгоритма RSA.
    """

    def __init__(self):
        rsa_file = list(map(int, open("RSA", "r", encoding="UTF-8").readlines()))

        self.__p = rsa_file[0]
        self.__q = rsa_file[1]

        self.__n = rsa_file[2]
        self.__f = rsa_file[3]
        self.__e = rsa_file[4]
        self.__d = pow(self.__e, -1, self.__f)

    def code(self, string: str):
        coded_symbols_list = [chr(ord(symbol) ** self.__e % self.__n) for symbol in string]
        return "".join(coded_symbols_list)

    def decode(self, coded_message: list):
        decoded_symbols_list = [chr(ord(symbol) ** self.__d % self.__n) for symbol in coded_message]
        return "".join(decoded_symbols_list)


class CryptoSHA256(metaclass=Singleton):
    @staticmethod
    def crypt(string: str, salt: str = "StandardSalt"):
        string_number = int(''.join([str(ord(symbol) * i) for i, symbol in enumerate(string, start=1)]))
        salt_number = int(''.join([str(ord(symbol) * i) for i, symbol in enumerate(salt, start=1)]))

        string_salted_text = str(string_number + salt_number)

        hash_string = string_salted_text
        for i in range(512):
            hash_string = sha256(hash_string.encode()).hexdigest()

        return hash_string
