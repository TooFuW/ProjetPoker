from Deck import Deck
from Hand import Hand
from Card import Card
import AlreadyExistingCard

if False:
    my_deck = Deck()

    print(my_deck)
    print("\n\n")

    my_deck.shuffle()

    print(my_deck, len(my_deck))
    print("\n\n")
    print(my_deck.draw(), len(my_deck))

if False:
    card = Card("spade","2")
    card2 = Card("spade","3")
    card3 = Card("spade","4")
    card4 = Card("spade","ace")

    print(card, card2, card==card2)
    hand = Hand([card,card2])
    hand2 = Hand([card3,card4])
    print(hand)
    print(type(hand.hand))
    print(hand+hand2)

card = Card("spade","2")
card2 = Card("spade","3")
card3 = Card("spade","4")
card4 = Card("spade","ace")

hand1 = Hand([card,card2])

hand1.get_hand().append("suii")
print(hand1)


