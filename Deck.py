import random
from Card import Card

class Deck:

    """
        Mutable and manipulable Deck of 52 cards
    """

    def __init__(self) -> None:
        self.deck = new_deck()


    
    def __str__(self) -> str:
        string = "["
        for card in self.deck:
            string += str(card)+", "
        string = string[0:-2]
        string+="]"

        return string
    

    def __len__(self):
        return len(self.deck)
    
    

    def draw(self):
        """
            Return the top card and remove it from the deck
        """
        top_card = self.deck[0]
        self.deck.remove(top_card)
        return(top_card)
    

    def shuffle(self):
        """
            Shuffle randomly and directly the deck 
        """

        random.shuffle(self.deck)
    
    




### Fonctions utilisées dans les méthodes ###



def new_deck():
    """
        Create a new deck of 52 non-shuffled cards
    """
    deck = []
    suits = ["club","heart","spade","diamond"]
    ranks = ["ace","2","3","4","5","6","7","8","9","10","jack","queen","king"]

    for suit in suits:
        for rank in ranks:
            deck.append(Card(suit,rank))

    return deck







        


    