from classes.player import Player


class Match(object):
    def __init__(self, players: dict = None, sets: dict = None, winner: Player = None) -> None:

        self.__players: dict = players

        self.__sets: dict = sets

        self.__winner: Player = winner

    def get_players(self) -> dict:
        return self.__players

    def get_sets(self) -> dict:
        return self.__sets

    def get_winner(self) -> Player:
        return self.__winner

    def set_players(self, player_a, player_b) -> None:
        self.__players['A'] = player_a
        self.__players['B'] = player_b

    def set_sets(self, set_a, set_b) -> None:
        self.__sets['A'] = set_a
        self.__sets['B'] = set_b

    def set_winner(self, winner):
        if winner not in self.get_players().keys():
            raise "winner has to be a key"
        self.__winner = winner
