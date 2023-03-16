from classes.competition_factory import Competition_factory
from classes.location import Location
from classes.prize import Prize
from datetime import datetime


class Tournament(object):
    def __init__(self, name: str, difficulty: float, location: Location, time: datetime, prizes: list) -> None:

        self.__name = name

        self.__difficulty = difficulty

        self.__location = location

        self.__time = time

        self.__prizes = prizes

        self.__competitions: list = list()

    def get_name(self) -> str:
        return self.__name
    
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

    def set_name(self, name: str) -> None:
        self.__name = name

    def set_difficulty(self, difficulty: float) -> None:
        self.__difficulty = difficulty

    def add_competition(self, t_type: str, players: list, matches: list) -> bool:
        self.__competitions.append(Competition_factory.get_competition_type(t_type)(players, matches))

    def update_prizes(self, prize, position) -> bool:
        try:
            self.__prizes[position-1] = prize
            return True
        except:
            return False


    def to_json(self,):
        tournament = []

        for c in self.__competitions:
            competition = {"rounds": [{"name": r, "matches":[]} for r in range(1,c.get_matches()[0].get_round()+1)]}
            print(competition)
            for m in c.get_matches():
                match = {"p1":{"name": m.get_players()["A"].get_name(), "score": m.get_sets()["A"]},"p2":{"name": m.get_players()["B"].get_name(), "score": m.get_sets()["B"]}, "winner": list(m.get_players().keys()).index(m.get_winner())+1}
                print(m.get_round())
                competition["rounds"][m.get_round()-1]["matches"].append(match)

            tournament.append(competition)
        return tournament
