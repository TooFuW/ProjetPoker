from Deck import Deck
from Hand import Hand
from Card import Card
import AlreadyExistingCard
from Player import Player
from Round import *
from Board import Board
import random

suits = ("spade","club","heart","diamond")
ranks = ("ace","2","3","4","5","6","7","8","9","10","jack","queen","king")
duo_list = []
combinations_list = []
print("\n")
for i in range(100):
    cards_used = []
    board_list = []
    hand_list = []

    while len(board_list) < 5:
        card = Card(suit=suits[random.randint(0,3)],rank=ranks[random.randint(0,12)])
        if card in cards_used:
            continue
        else:
            board_list.append(card)
            cards_used.append(card)

    while len(hand_list) < 2:
        card = Card(suit=suits[random.randint(0,3)],rank=ranks[random.randint(0,12)])
        if card in cards_used:
            continue
        else:
            hand_list.append(card)
            cards_used.append(card)

    duo_list.append((Board(board_list),Hand(hand_list)))

    print(f"Duo number {i+1}")
    print(duo_list[i][0],"   ", duo_list[i][1], "   ")
    combination = get_best_combination(duo_list[i][0],duo_list[i][1])[1][1]
    combinations_list.append(combination)
    print(combination)
    print("\n")

print(sorted([(3,2),(8,1),(3,4),(7,4)]))

combinations_list = sorted(combinations_list, reverse=True)
for combination in combinations_list:
    if combination.nature == "flush":
        print(combination)
        for i in combination.cards:
            print(i)
    else:
        print(combination)


    