from classes.tournament import Tournament


class Season(object):
    def __init__(self):
        self.__tournaments: list = list()

    def get_tournaments(self) -> list:

        return self.__tournaments

    def add_tournament(self, difficulty, location, time, prizes) -> None:
        self.__tournaments.append(Tournament(
            difficulty, location, time, prizes))
