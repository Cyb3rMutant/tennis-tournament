from abc import *


class User(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, id: int, name: str) -> None:

        self.__id: int = id

        self.__name: str = name

    @abstractmethod
    def get_id(self) -> int:
        return self.__id

    @abstractmethod
    def get_name(self) -> str:
        return self.__name
