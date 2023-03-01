from classes.player import Player


class Rankings(object):
    def __init__(self):
        self.__positions: list = list()

    def add_player(self, player: Player, position: int) -> bool:
        try:
            self.__positions.insert(position-1, player)
            return True
        except:
            return False

    def update_positions(self) -> bool:
        # ˅
        pass
