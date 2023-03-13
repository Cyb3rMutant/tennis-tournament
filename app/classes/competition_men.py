from classes.competition import Competition


class CompetitionMen(Competition):
    def __init__(self, players: list, matches: list) -> None:
        super().__init__(players, matches, 3)

    def evaluate_winner(self):
        pass
