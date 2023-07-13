from Deck import Deck
from Hand import Hand
from Card import Card
import AlreadyExistingCard
from Player import Player
from Round import is_royal_flush
from Round import is_straight_flush
from Round import is_straight_list
from Board import Board

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

if False:
    card = Card("spade","king")
    card2 = Card("spade","queen")
    card3 = Card("spade","jack")
    card4 = Card("spade","ace")
    card5 = Card("club","ace")

    board1 = Board([card,card3,card2,card4,card5])

    hand1 = Hand([Card("club","2"),Card("spade","10")])

    rh = Player(69,"rh",None, True, hand1,6900)

    rh.add_card(Card("spade","7"))
    print(rh.get_hand())
    print(rh.get_conn())
    print(rh.chips,rh.bank)
    rh.chips += 100
    rh.bank_remove(100)
    print(rh.chips,rh.bank)

    liste1 = hand1.get_hand()

    for i in liste1:
        print(i)

    print("\n")

    for i in sorted(liste1):
        print(i)

    print("\n")
    print(hand1)
    print(board1)
    print(is_royal_flush(board=board1, hand=hand1))



card = Card("spade","10")
card2 = Card("spade","9")
card3 = Card("spade","8")
card4 = Card("spade","6")
card5 = Card("club","ace")

board = Board([card,card2,card3,card4,card5])

hand1 = Hand([Card("club","2"),Card("spade","5")])

print(is_straight_flush(board=board, hand=hand1))


card = Card("spade","2")
card2 = Card("spade","3")
card3 = Card("spade","ace")
card4 = Card("spade","4")
card5 = Card("club","5")

board = Board([card,card2,card3,card4,card5])

hand1 = Hand([Card("club","6"),Card("spade","7")])

print(is_straight_list(board.get_board()+hand1.get_hand()))
print(is_straight_flush(board=board,hand=hand1))
