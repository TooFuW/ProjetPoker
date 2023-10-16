

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
            self.value = set_value(rank)
        else:
            raise ValueError
        

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"
    
    def __eq__(self, __value: object) -> bool:

        if type(__value) == Card:
            if (__value.rank == self.rank) and __value.suit == self.suit:
                return True
        return False
    
    def get_value(self):
        value_copy = self.value
        return value_copy
    
    def __lt__(self,card):
        if type(card) == Card:
            return self.value < card.get_value()
        else:
            return True
    
    def __mt__(self,card):
        if type(card) == Card:
            return self.value > card.get_value()
        return False
    
    def get_suit(self):
        copy = self.suit
        return copy
    
    def get_rank(self):
        copy = self.rank
        return copy


    




def is_new_card_valid(suit,rank):

    return suit in ("club","heart","spade","diamond") and rank in ("ace","2","3","4","5","6","7","8","9","10","jack","queen","king")
        
    
def set_value(rank):
    ranks = ("2","3","4","5","6","7","8","9","10","jack","queen","king","ace")
    for i in range (len(ranks)):
        if ranks[i] == rank:
            return i+2
    