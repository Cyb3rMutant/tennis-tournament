from abc import *


class User(metaclass=ABCMeta):
    def __init__(self, id: int, name: str) -> None:

        self.__id: int = id

        self.__name: str = name

    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name
