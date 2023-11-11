from typing import List
from Player import Player


class Pot :

    def __init__(self, mise : int = 0, sit_ids = List[int]) -> None:

        self.mise = mise
        self.sit_ids = sit_ids
        self.pot_closed = False

    def set_mise(self,mise):
        self.mise = mise

    def add_player(self,player : Player):
        self.sit_ids.append(player)

    def remove_player(self, player : Player):
        self.sit_ids.remove(player)

    def clear_players(self):
        self.sit_ids = []

    def __str__(self) -> str:
        """_summary_

        Returns:
            str: retourne la forme str du pot. un tuple associant le montant et la liste des joueurs dans le pot
        
        """
        return f"({str(self.mise)},{str(self.sit_ids)})"


    