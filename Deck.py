from deck_functions import *


class Deck:

    """
        Mutable and manipulable Deck of 52 cards
    """

    def __init__(self) -> None:
        self.deck = new_deck()
    
    def __str__(self) -> str:
        return str(self.deck)
        


    