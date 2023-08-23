from Deck import Deck
from Hand import Hand
from Card import Card
import AlreadyExistingCard
from Player import Player
from Round import *
from Board import Board
from Combination import Combination
from HandCombination import HandCombination
import random

suits = ("spade","club","heart","diamond")
ranks = ("ace","2","3","4","5","6","7","8","9","10","jack","queen","king")
duo_list = []
handcombinations_list = []
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
    handcombination = get_best_combination(duo_list[i][0],duo_list[i][1])[1]
    handcombinations_list.append(handcombination)
    print(handcombination, type(handcombination))
    print("\n")

    if handcombination.get_combination().nature == "royal_flush":
        break

handcombinations_list = sorted(handcombinations_list, reverse=True)
for combination in handcombinations_list:
    if combination.get_combination().nature == "flush":
        print(combination)
        for i in combination.get_combination().cards:
            print(i)
    else:
        print(combination)