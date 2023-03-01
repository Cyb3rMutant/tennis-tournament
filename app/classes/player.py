class Player(object):
    def __init__(self, id, name, ranking_points):

        self.__id: int = id

        self.__name: str = name

        self.__ranking_points: int = ranking_points

    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def get_ranking_points(self) -> int:
        return self.__ranking_points

    def update_ranking_points(self, points: int) -> None:
        self.__ranking_points += points
