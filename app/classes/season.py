from classes.tournament import Tournament
from bson.objectid import ObjectId


class Season(object):
    def __init__(self, id, name: str):
        self.__name: str = name
        self.__id: str = id
        self.__tournaments: dict= dict()

    def get_id(self):
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def get_tournaments(self) -> dict[ObjectId: Tournament]:
        return self.__tournaments

    def add_tournament(self, id, name, difficulty, prizes) -> None:
        self.__tournaments[id] = Tournament(id, name, difficulty, prizes)
