from Hand import Hand
from Board import Board
from Card import Card

class Round:
    """
        Represent a round (pre-flop to river) and manage winner players ...    
    
    """
    def __init__(self, players : list) -> None:
        pass
    def start(self):
        pass

    def start_pre_flop(self):
        pass

    def start_flop(self):
        pass

    def start_turn(self):
        pass

    def start_river(self):
        pass





def check_winner_hand(board : Board , hands : tuple):
    
    """
    
        Take a board and a tuple of hands and return the winning hand
    
    """
    pass

def is_royal_flush(hand : Hand, board : Board):
    board_list = board.get_board()
    hand_list = hand.get_hand()
    seven_cards_player = board_list+hand_list
    suits = ("club","heart","spade","diamond")
    for suit in suits:
        if Card(suit, "ace") in seven_cards_player:
            if Card(suit, "king") in seven_cards_player:
                if Card(suit, "queen") in seven_cards_player:
                    if Card(suit, "jack") in seven_cards_player:
                        if Card(suit, "10") in seven_cards_player:
                            return True
    return False

def is_straight_flush(hand : Hand, board : Board):
    board_list = board.get_board()
    hand_list = hand.get_hand()
    seven_cards_player = board_list+hand_list
    seven_cards_player = sorted(seven_cards_player)

    suits = ("club","heart","spade","diamond")

    cpt = 0
    for i in range(len(seven_cards_player)-1):
        current_suit = seven_cards_player[i].get_suit()
        print(seven_cards_player[i])
        if seven_cards_player[i+1].get_value() == seven_cards_player[i].get_value()+1 and seven_cards_player[i+1].get_suit() == current_suit:
            cpt +=1
            print(seven_cards_player[i],seven_cards_player[i+1], "enchainement ! cpt = ",cpt)
        else :
            cpt = 0
            print(seven_cards_player[i],seven_cards_player[i+1], "pas d'enchainement cpt = ",cpt)

        if cpt == 4:
            print("QUINTE FLUSH couleur : ", current_suit, "hauteur : ", seven_cards_player[i+1])
            return True

        if cpt == 3:
            if Card(current_suit, "ace") in seven_cards_player:
                print("QUINTE FLUSH HAUTEUR 5 couleur : ",current_suit)
                return True
    return False


def is_straight_list(seven_cards_player : list):
    seven_cards_player = sorted(seven_cards_player)
    cpt = 0
    for i in range(len(seven_cards_player)-1):
        print(seven_cards_player[i])
        if seven_cards_player[i+1].get_value() == seven_cards_player[i].get_value()+1:
            cpt +=1
            print(seven_cards_player[i],seven_cards_player[i+1], "enchainement ! cpt = ",cpt)

        elif seven_cards_player[i+1].get_value() == seven_cards_player[i].get_value():
            print(seven_cards_player[i],seven_cards_player[i+1], "meme valeur, on continue ! cpt = ",cpt)

        else:
            cpt = 0
            print(seven_cards_player[i],seven_cards_player[i+1], "pas d'enchainement ! cpt = ",cpt)

        if cpt == 4:
            print("QUINTE ! hauteur : ", seven_cards_player[i+1])
            return True

        if cpt == 3:
            if seven_cards_player[-1].rank == "ace":
                print("QUINTE HAUTEUR 5 ! ")
                return True
    return False


def is_straight(board : Board, hand : Hand):
    pass



        




