from classes.player import Player


class Match(object):
    def __init__(self, round: int, players: dict, sets: dict) -> None:
        self.__round: int = round

        self.__players: dict = players

        self.__sets: dict = sets

        self.__winner: str= sorted(self.__sets.items(), key= lambda i: i[1])[1][0]

    def get_round(self) -> int:
        return self.__round

    def get_players(self) -> dict:
        return self.__players

    def get_sets(self) -> dict:
        return self.__sets

    def get_winner(self) -> Player:
        return self.__winner
