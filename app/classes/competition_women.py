from classes.competition import Competition


class CompetitionWomen(Competition):
    def __init__(self, players: list, matches: list) -> None:
        super().__init__(players, matches, 2)
