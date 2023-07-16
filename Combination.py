from Card import Card

class Combination:
    def __init__(self,nature : str,high : str,suit=None ,second=None, cards=None) -> None:
        """_summary_

        Args:
            nature (str): high card, pair, straight, all the possible nature for a combination
            high (str): pair of 2 high will be 2, flush to ace high will be ace ...
            second (str) : if the combination is a full, will represent the pair, if its a two pair, will represent the low pair
            suit (str): suit of the combination
            cards (list): list of cards only if the combination type is flush

        Raises:
            ValueError: invalid values for high suit or nature
        """

        natures = ("high_card","pair","two_pair","three_of_a_kind","straight","flush","full_house","four_of_a_kind","straight_flush","royal_flush")
        highs = ("ace","2","3","4","5","6","7","8","9","10","jack","queen","king")
        display_highs = ("ace","two","three","four","five","six","seven","eight","nine","ten","jack","queen","king")
        suits = ("club","heart","spade","diamond")

        if nature not in natures or not high in highs or suit not in suits:
            raise ValueError
        
        self.nature = nature
        self.nature_value = nature.index(nature)+1          #une carte haute vaut 1, two pair vaut 3, full_house vaut 7 ...
        self.high = high
        self.display_high = display_highs[highs.index(high)]
        self.suit = suit

        if self.nature == "flush":

            if all([type(card) == Card for card in cards]):
                self.cards = cards

            else:
                raise TypeError
        
        if self.nature in ("full_house","two_pair"):
            if second in highs:
                self.second = second
                self.display_second = display_highs[highs.index(second)]

            else:
                raise ValueError


    def __str__(self):

        match self.nature:

            case "high_card":
                return self.display_high+" high"
            
            case "pair":
                return "pair of "+plural_display_high(self.display_high)
            
            case "two_pair":
                return "two pairs, "+self.display_high+" and "+self.second
            
            case "three_of_a_kind":
                return "three of a kind, "+plural_display_high(self.display_high)
            
            case "straight":
                return "straight with high card "+self.display_high
            
            case "flush":
                return "flush in "+self.suit+"s"
            
            case "full_house":
                return "full house with "+plural_display_high(self.display_high)+" over "+plural_display_high(self.display_second)
            
            case "four_of_a_kind":
                return "four of a kind, "+plural_display_high(self.display_high)
            
            case "straight_flush":
                return "straight flush in "+self.suit+"s"+" high card "+self.display_high
            
            case "royal_flush":
                return "royal_flush in "+self.suit+"s"
            



def plural_display_high(string):

    if string in ("ace","two","three","four","five","six","seven","eight","nine","ten","jack","queen","king"):
        if string == "six":
            return "sixes"
        else :
            return string+"s"
    else:
        return None


        
        
        