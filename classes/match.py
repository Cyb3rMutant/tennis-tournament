from classes.player import Player


class Match(object):
    def __init__(self, players: dict, sets: dict, winner: Player) -> None:

        self.__players: dict = players

        self.__sets: dict = sets

        self.__winner: Player = winner

    def get_players(self) -> dict:
        return self.__players

    def get_sets(self) -> dict:
        return self.__sets

    def get_winner(self) -> Player:
        return self.__winner

    def set_players(self, players) -> None:
        self.__players = players

    def set_sets(self, sets) -> None:
        self.__sets = sets

    def set_winner(self, winner: Player):
        self.__winner = winner
