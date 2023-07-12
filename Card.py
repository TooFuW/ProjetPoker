


class Card():

    """
    Represents a playing card.
    
    Attributes:
        suit (str): The suit of the card (e.g., "Spade", "Heart").
        rank (str): The rank of the card (e.g., "Ace", "King", "Queen").
    """
    
    def __init__(self,suit,rank) -> None:

        if is_new_card_valid(suit,rank):
            self.suit = suit
            self.rank = rank
        else:
            raise ValueError
        

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"
    
    def __eq__(self, __value: object) -> bool:

        if type(__value) == Card:
            if __value.suit == self.suit and __value.rank == self.rank:
                return True
        return False
    




def is_new_card_valid(suit,rank):

    if suit in ("club","heart","spade","diamond") and rank in ("ace","2","3","4","5","6","7","8","9","10","jack","queen","king"):
        return True
    else:
        return False