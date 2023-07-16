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



def get_best_combination(board : Board, hand : Hand):
    
    best_combination = is_royal_flush(board=board, hand=hand)

    if best_combination:
        return "royal flush",best_combination[1]
    
    best_combination = is_straight_flush(board=board,hand=hand)

    if best_combination:
        return "straight_flush",best_combination
    
    best_combination = is_four_of_a_kind(board=board,hand=hand)

    if best_combination:
        return "four of a kind",best_combination
    
    best_combination = is_full_house(board=board,hand=hand)

    if best_combination:
        return "full house",best_combination
    
    best_combination = is_flush(board=board,hand=hand)

    if best_combination:
        return "flush",best_combination
    
    best_combination = is_straight(board=board,hand=hand)

    if best_combination:
        return "straight",best_combination

    best_combination = is_three_of_a_kind(board=board,hand=hand)

    if best_combination:
        return "three of a kind",best_combination
    
    best_combination = is_two_pair(board=board,hand=hand)

    if best_combination:
        return "two pair",best_combination
    
    best_combination = is_one_pair(board=board,hand=hand)

    if best_combination:
        return "one pair",best_combination
    
    best_combination = high_card(board=board,hand=hand)
    return "high card", best_combination




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
                            return True,suit
    return False


def is_straight_flush(hand : Hand, board : Board):
    board_list = board.get_board()
    hand_list = hand.get_hand()
    seven_cards_player = board_list+hand_list
    seven_cards_player = sorted(seven_cards_player)

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
        is_straight = is_straight_list(heart_list)
        if is_straight:
            return is_straight
        
    if len(diamond_list) >= 5:
        is_straight = is_straight_list(diamond_list)
        if is_straight:
            return is_straight

    if len(club_list) >= 5:
        is_straight = is_straight_list(club_list)
        if is_straight:
            return is_straight

    if len(spade_list) >= 5:
        is_straight = is_straight_list(spade_list)
        if is_straight:
            return is_straight
        
    return False


def is_four_of_a_kind(board : Board, hand : Hand):

    board_list = board.get_board()
    hand_list = hand.get_hand()
    seven_cards_player = board_list+hand_list
    seven_cards_player = sorted(seven_cards_player)

    current_rank = seven_cards_player[0].get_rank()
    current_count = 1

    for i in range(len(seven_cards_player)-1):
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
    seven_cards_player = sorted(seven_cards_player, reverse=True)

    pair = False
    three_of_a_kind = False

    cpt = 1

    for i in range(len(seven_cards_player)-1):
        
        if seven_cards_player[i+1].get_rank() == seven_cards_player[i].get_rank():
            cpt += 1
        else:
            if cpt == 2 and not pair:
                pair = True,seven_cards_player[i].get_rank()
                cpt = 1

            if cpt >= 3:
                if not three_of_a_kind:
                    three_of_a_kind = True, seven_cards_player[i].get_rank()
                    cpt = 1
                elif not pair:
                    pair = True,seven_cards_player[i].get_rank()
                    

            else:
                cpt = 1

            if three_of_a_kind and pair:
                return True,(three_of_a_kind[1],pair[1])

    if cpt == 2 and not pair:
            pair = True,seven_cards_player[-1].get_rank()
            cpt = 1

    if cpt >= 3:
        if not three_of_a_kind:
            three_of_a_kind = True, seven_cards_player[-1].get_rank()
            cpt = 1
        else:
            pair = True,seven_cards_player[-1].get_rank()

    
    if three_of_a_kind and pair:
        return True, (three_of_a_kind[1],pair[1])
    else:
        return False
    

def is_flush(board : Board, hand : Hand):

    liste = board.get_board()+hand.get_hand()
    suit_list = [card.get_suit() for card in liste]
    for suit in suit_list:
        if suit_list.count(suit) >= 5:
            return True,suit
        
    return False


def is_straight_list(seven_cards_player : list):   # Vérifie la présence d'une quinte avec un board et une main

    seven_cards_player = sorted(seven_cards_player)
    cpt = 0

    for i in range(len(seven_cards_player)-1):
        if seven_cards_player[i+1].get_value() == seven_cards_player[i].get_value()+1:
            cpt +=1

        elif seven_cards_player[i+1].get_value() == seven_cards_player[i].get_value():
            pass

        else:
            if cpt >= 4:
                return True,seven_cards_player[i].get_rank()

            if cpt == 3 and seven_cards_player[i].get_value() == 5:
                if seven_cards_player[-1].rank == "ace":
                    return True,5
            cpt = 0

    if cpt >= 4:
        return True,seven_cards_player[-1].get_rank()

    if cpt == 3 and seven_cards_player[-1].get_value() == 5:
        if seven_cards_player[-1].rank == "ace":
            return True,5
    return False


def is_straight(board : Board, hand : Hand):
    liste = board.get_board()+hand.get_hand()
    return is_straight_list(liste)
    

def is_three_of_a_kind(board : Board, hand : Hand): #parcours la liste 1 fois et trouve le plus haut brelan
    liste = board.get_board()+hand.get_hand()
    liste = sorted(liste, reverse=True)
    liste = [card.get_rank() for card in liste]

    cpt = 1

    for i in range(1,len(liste)):
        if liste[i] == liste[i-1]:
            cpt += 1
        else:
            cpt = 1
        
        if cpt == 3:
            return True,liste[i]
        
    return False


def is_two_pair(board : Board, hand : Hand):
    liste = board.get_board()+hand.get_hand()
    liste = sorted(liste, reverse=True)
    liste = [card.get_rank() for card in liste]

    high_pair = False
    low_pair = False
    cpt = 1

    for i in range(1,len(liste)):
        if liste[i] == liste[i-1]:
            cpt += 1
        else:
            if cpt >=2 :
                if not high_pair:
                    high_pair = True, liste[i-1]

                elif not low_pair:
                    low_pair = True, liste[i-1]
                
            cpt = 1

        
        if high_pair and low_pair:
            return True,(high_pair[1],low_pair[1])
        
    if cpt >=2 :
                if not high_pair:
                    high_pair = True, liste[i-1]

                elif not low_pair:
                    low_pair = True, liste[i-1]

    if high_pair and low_pair:
            return True,(high_pair[1],low_pair[1])
    else:      
        return False


def is_one_pair(board : Board, hand : Hand):
    liste = board.get_board()+hand.get_hand()
    liste = sorted(liste, reverse=True)
    liste = [card.get_rank() for card in liste]
    len_list = len(liste)
    cpt = 1

    for i in range(len_list):
        if i < len_list-1:
            if liste[i] == liste[i+1]:
                cpt +=1
        if cpt == 2:
            return True,liste[i]
        
    return False


def high_card(board: Board, hand : Hand):
    liste = board.get_board()+hand.get_hand()
    return max(liste).get_rank()
            

        




