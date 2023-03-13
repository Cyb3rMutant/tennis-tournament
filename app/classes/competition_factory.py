from classes.competition_men import CompetitionMen
from classes.competition_women import CompetitionWomen


class Competition_factory(object):
    @staticmethod
    def get_competition_type(type: str):
        types = {"M": CompetitionMen,
                 "F": CompetitionWomen}

        if type not in types:
            raise Exception("%s competition type does not exist" % type)

        return types[type]
