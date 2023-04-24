from abc import *


class Competition(object, metaclass=ABCMeta):
    def __init__(self, players: list, matches: list, sets_to_win: int) -> None:

        self._players: list = list()

        self._sets_to_win: int = sets_to_win

        self._matches = matches

    def get_players(self) -> list:
        return self._players

    def get_sets_to_win(self) -> int:
        return self._sets_to_win

    def get_matches(self) -> list:
        return self._matches

    def set_players(self, players) -> None:
        self._players = players

    def set_sets_to_win(self, sets_to_win: int) -> int:
        self._sets_to_win = sets_to_win

    def set_matches(self, matches) -> None:
        self._matches = matches
