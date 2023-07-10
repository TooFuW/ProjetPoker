from Card import Card
import AlreadyExistingCard

class Hand:

    def __init__(self,hand : list) -> None:

        if type(hand) != list:          # hand must be a list
            raise TypeError

        if only_card_list(hand):
            if not is_card_duplicate(hand):    # hand must only contain unique cards 
                self.hand = hand
            else:
                raise AlreadyExistingCard
        else:
            raise ValueError
        
        
    def __str__(self) -> str:
        if self.hand == []:
            return "[]"
        
        string = "["
        for i in self.hand:
            string += str(i)+", "
        string = string[0:-2]
        string += "]"

        return string
    
    def add_card(self, card : Card):

        if type(card) == Card:
            if not card_in_list(self.hand,card):
                self.hand.append(card)
            else:
                raise AlreadyExistingCard
        else:
            raise TypeError

            
        



def only_card_list(hand : list):
    if hand == []:
        return True
    
    for i in hand:
        if type(i) != Card:
            return False
    return True


def is_card_duplicate(hand : list):
    if hand == []:
        return False
    
    for i in hand:
        if hand.count(i) > 1:
            return True
    
    return False

def card_in_list(liste : list ,card : Card):
    return card in liste


