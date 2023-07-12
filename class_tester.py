from Deck import Deck
from Hand import Hand
from Card import Card
import AlreadyExistingCard
from Player import Player

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

if False:
    i = 0
    while True:
        print (i)
        if i%2 == 0:
            print("pair")
        else:
            print("impair")
        i += 1
        if i == 1469 :
            break


card = Card("spade","2")
card2 = Card("spade","3")
card3 = Card("spade","4")
card4 = Card("spade","ace")

hand1 = Hand([card,card2])

rh = Player(69,"rh",None, True, hand1,6900)

rh.add_card(Card("spade","7"))
print(rh.get_hand())
print(rh.get_conn())
print(rh.chips,rh.bank)
rh.chips += 100
rh.bank_remove(100)
print(rh.chips,rh.bank)