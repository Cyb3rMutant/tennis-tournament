from abc import *
from classes.match import Match
from classes.player import Player


class Competition(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, players: list, matches: list) -> None:

        self.__players: list = list()

        self.__matches: list = list()

    @abstractmethod
    def get_players(self) -> list:
        return self.__players

    @abstractmethod
    def get_matches(self) -> list:

        return self.__matches

    @abstractmethod
    def set_players(self, players) -> None:
        self.__players = players

    @abstractmethod
    def set_matches(self, matches) -> None:
        self.__matches = matches

    @abstractmethod
    def evaluate_winner(self):
        # ˅
        pass
