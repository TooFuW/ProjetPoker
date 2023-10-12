from typing import List
from Player import Player


class Pot :

    def __init__(self, mise : int = 0, players : List[Player] = []) -> None:

        self.mise = mise
        self.players = players

    def set_mise(self,mise):
        self.mise = mise

    def add_player(self,player : Player):
        self.players.append(player)

    def remove_player(self, player : Player):
        self.players.remove(player)

    def clear_players(self):
        self.players = []

    