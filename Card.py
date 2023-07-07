


class Card():

    """
    Represents a playing card.
    
    Attributes:
        suit (str): The suit of the card (e.g., "Spades", "Hearts").
        rank (str): The rank of the card (e.g., "Ace", "King", "Queen").
    """
    
    def __init__(self,suit,rank) -> None:
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"