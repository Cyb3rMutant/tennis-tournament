from classes.competition_factory import Competition_factory


class Tournament(object):
    def __init__(self, id,  name: str, difficulty: float, prizes: list) -> None:

        self.__id = id

        self.__name = name

        self.__difficulty = difficulty
        print(difficulty, type(difficulty))

        self.__prizes = prizes

        self.__competitions: list = list()

    def get_id(self):
        return self.__id

    def get_name(self) -> str:
        return self.__name
    
    def get_difficulty(self) -> float:
        return self.__difficulty

    def get_prizes(self) -> list:
        return self.__prizes

    def get_competitions(self) -> list:
        return self.__competitions

    def add_competition(self, t_type: str, players: list, matches: list) -> bool:
        self.__competitions.append(Competition_factory.get_competition_type(t_type)(players, matches))

    def clear(self):
        print("clearing")
        self.__competitions =[]

    def to_json(self,):
        tournament = []

        for c in self.__competitions:
            competition = {"rounds": [{"name": r, "matches":[]} for r in range(1,c.get_matches()[0].get_round()+1)]}
            for m in c.get_matches():
                match = {"p1":{"name": m.get_players()["A"].get_name(), "score": m.get_sets()["A"]},"p2":{"name": m.get_players()["B"].get_name(), "score": m.get_sets()["B"]}, "winner": list(m.get_players().keys()).index(m.get_winner())+1}
                competition["rounds"][m.get_round()-1]["matches"].append(match)

            tournament.append(competition)
        return tournament
