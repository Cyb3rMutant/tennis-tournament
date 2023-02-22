from classes.competition import Competition
from classes.location import Location
from classes.prize import Prize
from classes.datetime import datetime


class Tournament(object):
    def __init__(self, difficulty: float, location: Location, time: datetime, prizes: list) -> None:

        self.__difficulty = difficulty

        self.__location = location

        self.__time = time

        self.__prizes = prizes

        self.__competitions: list = list()

    def get_difficulty(self) -> float:
        return self.__difficulty

    def get_location(self) -> Location:
        return self.__location

    def get_time(self) -> datetime:
        return self.__time

    def get_prizes(self) -> list:

        return self.__prizes

    def get_competitions(self) -> list:
        return self.__competitions

    def set_difficulty(self, difficulty: float) -> None:
        self.__difficulty = difficulty

    def add_competition(self, players: list, matches: list) -> bool:
        try:
            self.__competitions.append(Competition(players, matches))
            return True
        except:
            return False

    def update_prizes(self, prize, position) -> bool:
        try:
            self.__prizes[position-1] = prize
            return True
        except:
            return False
