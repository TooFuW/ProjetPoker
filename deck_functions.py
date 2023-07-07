from Card import Card


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