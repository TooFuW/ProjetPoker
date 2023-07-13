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

    heart_list, spade_list, club_list, diamond_list = [],[],[],[]

    for card in seven_cards_player:
        if card.get_suit() == "club":
            club_list.append(card)

        if card.get_suit() == "heart":
            heart_list.append(card)

        if card.get_suit() == "diamond":
            diamond_list.append(card)

        if card.get_suit() == "spade":
            spade_list.append(card)

    
    if len(heart_list) >= 5:
        if is_straight_list(heart_list):
            print("QUINTE FLUSH COULEUR COEUR")
            return True
        
    if len(diamond_list) >= 5:
        if is_straight_list(diamond_list):
            print("QUINTE FLUSH COULEUR CARREAU")
            return True

    if len(club_list) >= 5:
        if is_straight_list(club_list):
            print("QUINTE FLUSH COULEUR TREFLE")
            return True

    if len(spade_list) >= 5:
        if is_straight_list(spade_list):
            print("QUINTE FLUSH COULEUR PIQUE")
            return True
        
    return False


    


def is_straight_list(seven_cards_player : list):   # Vérifie la présence d'une quinte avec un board et une main

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
            if cpt >= 4:
                print("QUINTE ! hauteur : ", seven_cards_player[i])
                return True,seven_cards_player[-1]

            if cpt == 3 and seven_cards_player[i].get_value() == 5:
                if seven_cards_player[-1].rank == "ace":
                    print("QUINTE HAUTEUR 5 ! ")
                    return True,5
            cpt = 0
            print(seven_cards_player[i],seven_cards_player[i+1], "pas d'enchainement ! cpt = ",cpt)

    if cpt >= 4:
        print("QUINTE ! hauteur : ", seven_cards_player[-1])
        return True,seven_cards_player[-1]

    if cpt == 3 and seven_cards_player[-1].get_value() == 5:
        if seven_cards_player[-1].rank == "ace":
            print("QUINTE HAUTEUR 5 ! ")
            return True,5
    return False


def is_straight(board : Board, hand : Hand):
    liste = board.get_board()+hand.get_hand()
    return is_straight_list(liste)
    

def is_four_of_a_kind(board : Board, hand : Hand):

    board_list = board.get_board()
    hand_list = hand.get_hand()
    seven_cards_player = board_list+hand_list
    seven_cards_player = sorted(seven_cards_player)

    current_rank = seven_cards_player[0].get_rank()
    current_count = 1

    for i in range(len(seven_cards_player)-1):
        print(current_rank,current_count)
        if seven_cards_player[i].get_value() == seven_cards_player[i+1].get_value():
            current_count += 1
        else:
            current_count = 1
            current_rank = seven_cards_player[i+1].get_rank()
    
    if current_count == 4:
        return True,current_rank
    
    return False

def is_full_house(board : Board, hand : Hand):

    board_list = board.get_board()
    hand_list = hand.get_hand()
    seven_cards_player = board_list+hand_list
    seven_cards_player = sorted(seven_cards_player).reverse()

    for i in range(len(seven_cards_player)-1):
        pass

        




