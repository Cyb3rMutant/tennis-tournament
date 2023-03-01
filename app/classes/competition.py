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
    @abstractmethod
    def __init__(self, players: list, matches: list, sets_to_win: int) -> None:

        self.__players: list = list()

        self.__sets_to_win: int = sets_to_win

        self.__matches: Match = MatchTree()

    @abstractmethod
    def get_players(self) -> list:
        return self.__players

    @abstractmethod
    def get_sets_to_win(self) -> int:
        return self.__sets_to_win

    @abstractmethod
    def get_matches(self) -> list:
        return self.__matches

    @abstractmethod
    def set_players(self, players) -> None:
        self.__players = players

    @abstractmethod
    def set_sets_to_win(self, sets_to_win: int) -> int:
        self.__sets_to_win = sets_to_win

    @abstractmethod
    def set_matches(self, matches) -> None:
        self.__matches = matches

    @abstractmethod
    def evaluate_winner(self):
        pass
