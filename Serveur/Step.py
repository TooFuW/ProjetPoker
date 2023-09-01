from Board import Board
from Deck import Deck
from Sit import Sit
from typing import List
class Step:
    """

        Represent a step of the game (pre-flop, flop, turn, river) and call the methods for each player

    """
    def __init__(self,type : str ,sits : List[Sit], board : Board, deck : Deck) -> None: # Les sièges doivent être edit par le lobby à chaque changement
        self.type = type
        self.sits = sits
        self.board = board
        self.deck = deck
        print(id(self.board))

    def start(self):
        pass

    def stop(self):
        pass

    def edit_sits(self,new_sits : List[Sit]):
        self.sits = new_sits

    def flop_board(self):
        for _ in range(3):
            card = self.deck.draw()
            self.board.add_card(card)

    def turn_board(self):
        card = self.deck.draw()
        self.board.add_card(card)

    def river_board(self):
        card = self.deck.draw()
        self.board.add_card(card)


