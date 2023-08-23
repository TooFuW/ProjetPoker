from Hand import Hand
from Board import Board
from Card import Card
from Deck import Deck
from Combination import Combination
from HandCombination import HandCombination

class Round:
    """
        Represent a round (pre-flop to river) and manage winner players ... 

        important : deck est la pioche de cartes avec laquelle on va créer les mains et distributions 
        hand_combinations est un dictionnaire qui associe un player_id à sa HandCombination c'est ce qui permettra de tout comparer à la fin  
    
    """
    def __init__(self, players : list, dealer_id : int) -> None:
        self.players = players
        self.dealer_id = dealer_id

        self.deck = new_shuffled_deck()
        self.board = Board()

        self.hand_combinations = {}


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


    def set_hands(self):
        for player in self.players:
            new_hand_list = []
            for _ in range(2):
                new_hand_list.append(self.deck.draw())
            
            new_hand = Hand(new_hand_list)
            player.set_hand(new_hand)

    def set_hand_combinations(self):
        for pl in self.players:
            pl_id = pl.get_id()
            pl_hand = pl.get_hand()

            self.hand_combinations[pl_id] = get_best_combination(board=self.board, hand=pl_hand)[1] #le [1] permet d'avoir l'objet HandCombination et pas la str qui donne le titre de la combination

    def players_best_combination(self):
        hand_combinations = [el for el in self.hand_combinations.values()]
        best_hand_combination = max(hand_combinations)
        best_players_combination = []

        for pl_id in self.hand_combinations.keys():
            if not self.hand_combinations[pl_id] < best_hand_combination:
                best_players_combination.append(pl_id)
                
        return best_players_combination






def new_shuffled_deck():
    deck = Deck()
    deck.shuffle()
    print(deck)
    return deck


def get_best_combination(board : Board, hand : Hand):
    """Renvoie à partir d'un board et d'une hand la meilleure HandCombination possible.

    Args:
        board (Board): _description_
        hand (Hand): _description_

    Returns:
        _type_: Tuple(nom de la combinaison, HandCombination correspondante)
    """
    
    best_combination = is_royal_flush(board=board, hand=hand)

    if best_combination:
        return "royal flush",best_combination[1]
    
    best_combination = is_straight_flush(board=board,hand=hand)

    if best_combination:
        return "straight_flush",best_combination[1]
    
    best_combination = is_four_of_a_kind(board=board,hand=hand)

    if best_combination:
        return "four of a kind",best_combination[1]
    
    best_combination = is_full_house(board=board,hand=hand)

    if best_combination:
        return "full house",best_combination[1]
    
    best_combination = is_flush(board=board,hand=hand)

    if best_combination:
        return "flush",best_combination[1]
    
    best_combination = is_straight(board=board,hand=hand)

    if best_combination:
        return "straight",best_combination[1]

    best_combination = is_three_of_a_kind(board=board,hand=hand)

    if best_combination:
        return "three of a kind",best_combination[1]
    
    best_combination = is_two_pair(board=board,hand=hand)

    if best_combination:
        return "two pair",best_combination[1]
    
    best_combination = is_one_pair(board=board,hand=hand)

    if best_combination:
        return "one pair",best_combination[1]
    
    best_combination = high_card(board=board,hand=hand)
    return "high card", best_combination[1]




def check_winner_hand(board : Board , hands : tuple):
    
    """
    
        Take a board and a tuple of hands and return the winning hand
    
    """
    pass


def is_royal_flush(hand : Hand, board : Board):
    """Si le hand et le board forment une quinte flush royale renvoie True et le HandCombination correspondante. False sinon

    Args:
        hand (Hand): main du joueur
        board (Board): cartes communes objet Board

    Returns:
        _type_: renvoie un Booléen et si True renvoie le HandCombination correspondant à la quinte flush
    """
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
                            return True,HandCombination([Combination("royal_flush",Card(suit,"ace"),suit)])
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
            return True,HandCombination([Combination("straight_flush",is_straight[1].hand_combination[0].high,"heart")])
        
    if len(diamond_list) >= 5:
        is_straight = is_straight_list(diamond_list)
        if is_straight:
            return True,HandCombination([Combination("straight_flush",is_straight[1].hand_combination[0].high,"diamond")])

    if len(club_list) >= 5:
        is_straight = is_straight_list(club_list)
        if is_straight:
            return True,HandCombination([Combination("straight_flush",is_straight[1].hand_combination[0].high,"club")])

    if len(spade_list) >= 5:
        is_straight = is_straight_list(spade_list)
        if is_straight:
            return True,HandCombination([Combination("straight_flush",is_straight[1].hand_combination[0].high,"spade")])
        
    return False


def is_four_of_a_kind(board : Board, hand : Hand):

    board_list = board.get_board()
    hand_list = hand.get_hand()
    seven_cards_player = board_list+hand_list
    seven_cards_player = sorted(seven_cards_player)

    current_count = 1

    for i in range(len(seven_cards_player)-1):
        if seven_cards_player[i].get_value() == seven_cards_player[i+1].get_value():
            current_count += 1
        else:
            current_count = 1
            

        if current_count == 4:
            return True,HandCombination([Combination("four_of_a_kind",seven_cards_player[i]),seven_cards_player[i-3]])  # retourne carré de ... ainsi que la 5eme carte de la main
    
    if current_count == 4:
        return True,HandCombination([Combination("four_of_a_kind",seven_cards_player[-1]),seven_cards_player[-5]]) # retourne carré de ... ainsi que la 5eme carte de la main
    
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
                pair = True,seven_cards_player[i]
                cpt = 1

            if cpt >= 3:
                if not three_of_a_kind:
                    three_of_a_kind = True, seven_cards_player[i]
                    cpt = 1
                elif not pair:
                    pair = True,seven_cards_player[i]
                    

            else:
                cpt = 1

            if three_of_a_kind and pair:
                return True,HandCombination([Combination("full_house",high=three_of_a_kind[1], second=pair[-1])])

    if cpt == 2 and not pair:
            pair = True,seven_cards_player[-1]
            cpt = 1

    if cpt >= 3:
        if not three_of_a_kind:
            three_of_a_kind = True, seven_cards_player[-1]
            cpt = 1
        else:
            pair = True,seven_cards_player[-1]

    
    if three_of_a_kind and pair:
        return True,HandCombination([Combination("full_house",high=three_of_a_kind[1], second=pair[-1])])
    else:
        return False
    

def is_flush(board : Board, hand : Hand):

    liste = board.get_board()+hand.get_hand()
    suit_list = [card.get_suit() for card in liste]
    for suit in suit_list:
        if suit_list.count(suit) >= 5:
            flush_cards = [card for card in liste if card.get_suit()==suit]
            return True,HandCombination([Combination("flush",max(flush_cards),suit,cards=flush_cards)])
        
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
                return True,HandCombination([Combination("straight",seven_cards_player[i])])

            if cpt == 3 and seven_cards_player[i].get_value() == 5:
                if seven_cards_player[-1].rank == "ace":
                    return True,HandCombination([Combination("straight",seven_cards_player[i])])
            cpt = 0

    if cpt >= 4:
        return True,HandCombination([Combination("straight",seven_cards_player[-1])])

    if cpt == 3 and seven_cards_player[-1].get_value() == 5:
        if seven_cards_player[-1].rank == "ace":
            return True,HandCombination([Combination("straight",seven_cards_player[-1])])
        
    return False


def is_straight(board : Board, hand : Hand):
    liste = board.get_board()+hand.get_hand()
    return is_straight_list(liste)
    

def is_three_of_a_kind(board : Board, hand : Hand): #parcours la liste 1 fois et trouve le plus haut brelan
    liste = board.get_board()+hand.get_hand()
    liste = sorted(liste, reverse=True)

    cpt = 1

    for i in range(1,len(liste)):
        if liste[i].get_rank() == liste[i-1].get_rank():
            cpt += 1
        else:
            cpt = 1
        
        if cpt == 3:
            return True,HandCombination([Combination("three_of_a_kind",liste[i])]+[card for card in liste if card.get_rank() != liste[i].get_rank()])
        
    if cpt == 3:
            return True,[Combination("three_of_a_kind",liste[-1])]+[card for card in liste if card.get_rank() != liste[-1].get_rank()]
    
    return False


def is_two_pair(board : Board, hand : Hand):
    liste = board.get_board()+hand.get_hand()
    liste = sorted(liste, reverse=True)

    high_pair = False
    low_pair = False
    cpt = 1

    for i in range(1,len(liste)):
        if liste[i].get_rank() == liste[i-1].get_rank():
            cpt += 1
        else:
            if cpt >=2 :
                if not high_pair:
                    high_pair = True, liste[i-1]

                elif not low_pair:
                    low_pair = True, liste[i-1]
                
            cpt = 1

        
        if high_pair and low_pair:
            return True,HandCombination([Combination("two_pair",high=high_pair[1], second=low_pair[1])]+[card for card in liste if card.get_rank() != high_pair[1].get_rank() and card.get_rank() != low_pair[1].get_rank()])
        
    if cpt >=2 :
                if not high_pair:
                    high_pair = True, liste[i-1]

                elif not low_pair:
                    low_pair = True, liste[i-1]

    if high_pair and low_pair:
            return True,HandCombination([Combination("two_pair",high=high_pair[1], second=low_pair[1])]+[card for card in liste if card.get_rank() != high_pair[1].get_rank() and card.get_rank() != low_pair[1].get_rank()])
    else:      
        return False


def is_one_pair(board : Board, hand : Hand):
    liste = board.get_board()+hand.get_hand()
    liste = sorted(liste, reverse=True)

    len_list = len(liste)
    cpt = 1

    for i in range(len_list):
        if i < len_list-1:
            if liste[i].get_rank() == liste[i+1].get_rank():
                cpt +=1
        if cpt == 2:
            print(liste, "YOOOO")
            return True,HandCombination([Combination("pair",liste[i])]+[card for card in liste if card.get_rank() != liste[i].get_rank()])
        
    return False


def high_card(board: Board, hand : Hand):
    liste = board.get_board()+hand.get_hand()
    max_liste = max(liste)
    return True,HandCombination([Combination("high_card",max_liste)]+[card for card in liste if card.get_rank() != max_liste.get_rank()])
            

        




