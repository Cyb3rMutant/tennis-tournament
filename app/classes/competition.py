from abc import *
from classes.match import Match
from classes.player import Player
from binarytree import Node


class MatchTree():
    def __init__(self, depth):
        queue = []
        tree_depth = 1
        self.root = Node(Match())
        queue.append(self.root)

        while (tree_depth > depth) and (size := len(queue)):
            for i in range(size):
                node = queue.pop(0)
                node.left = Node(Match())
                node.right = Node(Match())
                queue.append(node.left)
                queue.append(node.right)
            tree_depth += 1
        print(self.root)


class Competition(object, metaclass=ABCMeta):
    def __init__(self, players: list, matches: list, sets_to_win: int) -> None:

        self._players: list = list()

        self._sets_to_win: int = sets_to_win

        self._matches = matches

        # self._matches: Match = MatchTree()

    def get_players(self) -> list:
        return self._players

    def get_sets_to_win(self) -> int:
        return self._sets_to_win

    def get_matches(self) -> list:
        return self._matches

    def set_players(self, players) -> None:
        self._players = players

    def set_sets_to_win(self, sets_to_win: int) -> int:
        self._sets_to_win = sets_to_win

    def set_matches(self, matches) -> None:
        self._matches = matches

