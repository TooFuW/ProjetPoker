from Card import Card

class Combination:
    def __init__(self,nature : str,high : Card,suit=None ,second=None, cards=None) -> None:
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
        natures_card_occupation = (1,2,4,3,5,5,5,4,5,5)
        highs = ("ace","2","3","4","5","6","7","8","9","10","jack","queen","king")
        display_highs = ("ace","two","three","four","five","six","seven","eight","nine","ten","jack","queen","king")
        suits = ("club","heart","spade","diamond",None)

        if not nature in natures or not high.get_rank() in highs or not suit in suits:
            print(not nature in natures)
            print(not high.get_rank() in highs)
            print(not suit in suits)
            raise ValueError
        
        self.nature = nature
        self.nature_value = natures.index(nature)+1
        self.nature_card_occupation = natures_card_occupation[natures.index(self.nature)]

        self.high = high

        self.display_high = display_highs[highs.index(high.get_rank())]
        self.suit = suit

        if self.nature == "flush":

            if all([type(card) == Card for card in cards]):
                self.cards = cards
                self.cards = sorted(self.cards, reverse=True)

            else:
                raise TypeError
        
        if self.nature in ("full_house","two_pair"):
            if second.get_rank() in highs:
                self.second = second
                self.display_second = display_highs[highs.index(second.get_rank())]

            else:
                raise ValueError


    def __str__(self):

        match self.nature:

            case "high_card":
                return self.display_high+" high"
            
            case "pair":
                return "pair of "+plural_display_high(self.display_high)
            
            case "two_pair":
                return "two pairs, "+self.display_high+" and "+self.display_second
            
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
            

    def __eq__(self,__value : object):
        if type(__value) == Combination:

            if self.nature == __value.nature:

                match self.nature:

                    case "high_card":
                        return self.high.get_rank() == __value.high.get_rank()
                    
                    case "pair":
                        return self.high.get_rank() == __value.high.get_rank()
                    
                    case "two_pair":
                        return self.high.get_rank() == __value.high.get_rank() and self.second.get_rank() == __value.second.get_rank()
                    
                    case "three_of_a_kind":
                        return self.high.get_rank() == __value.high.get_rank()
                    
                    case "straight":
                        return self.high.get_rank() == __value.high.get_rank()
                    
                    case "flush":
                        for i in range(len(self.cards)):
                            if self.cards[i].get_rank() != __value.cards[i].get_rank():
                                return False
                        return True
                    
                    case "full_house":
                        return self.high.get_rank() == __value.high.get_rank() and self.second.get_rank() == __value.second.get_rank()
                    
                    case "four_of_a_kind":
                        return self.high.get_rank() == __value.high.get_rank()
                    
                    case "straight_flush":
                        return self.high.get_rank() == __value.high.get_rank()
                    
                    case "royal_flush":
                        return self.high.get_rank() == __value.high.get_rank()
            else:
                return False
                
        else:
            if type(__value) == Card:
                return False
            else:
                raise TypeError
        
    
    def __mt__(self, __value : object):
        
        if type(__value) == Combination:

            if self.nature_value > __value.nature_value:
                return True
            elif self.nature_value < __value.nature_value:
                return False
            
            else:

                match self.nature:

                    case "high_card":
                        return self.high > __value.high
                    
                    case "pair":
                        return self.high.get_value() > __value.high.get_value()
                    
                    case "two_pair":

                        if self.high > __value.high:
                            return True
                        
                        elif self.high < __value.high:
                            return False
                        
                        else:

                            if self.second > __value.second:
                                return True
                            elif self.second < __value.second:
                                return False
                            else:
                                return False
                    

                    case "three_of_a_kind":
                        return self.high > __value.high
                    
                    case "straight":
                        return self.high >  __value.high
                    
                    case "flush":
                        for i in range(len(self.cards)):
                            if self.cards[i] > __value.cards[i]:
                                return True
                            elif self.cards[i] < __value.cards[i]:
                                return False
                        return False
                    
                    case "full_house":
                        if self.high > __value.high:
                            return True
                        elif self.high < __value.high:
                            return False
                        else:
                            if self.second > __value.second:
                                return True
                            elif self.second < __value.second:
                                return False
                            else:
                                return False
                    
                    case "four_of_a_kind":
                        return self.high > __value.high
                    
                    case "straight_flush":
                        return self.high > __value.high
                    
                    case "royal_flush":
                        return self.high > __value.high

        else:
            if type(__value) == Card:
                return True
            else:
                raise TypeError


    def __lt__(self, __value : object):
        if type(__value) == Combination:

            if self.nature_value < __value.nature_value:
                return True
            elif self.nature_value > __value.nature_value:
                return False
            
            else:

                match self.nature:

                    case "high_card":
                        return self.high < __value.high
                    
                    case "pair":
                        return self.high < __value.high
                    
                    case "two_pair":

                        if self.high < __value.high:
                            return True
                        
                        elif self.high > __value.high:
                            return False
                        
                        else:

                            if self.second < __value.second:
                                return True
                            elif self.second > __value.second:
                                return False
                            else:
                                return False
                    

                    case "three_of_a_kind":
                        return self.high < __value.high
                    
                    case "straight":
                        return self.high <  __value.high
                    
                    case "flush":
                        for i in range(len(self.cards)):
                            if self.cards[i] < __value.cards[i]:
                                return True
                            elif self.cards[i] > __value.cards[i]:
                                return False
                        return False
                    
                    case "full_house":
                        if self.high < __value.high:
                            return True
                        elif self.high > __value.high:
                            return False
                        else:
                            if self.second < __value.second:
                                return True
                            elif self.second > __value.second:
                                return False
                            else:
                                return False
                    
                    case "four_of_a_kind":
                        return self.high < __value.high
                    
                    case "straight_flush":
                        return self.high < __value.high
                    
                    case "royal_flush":
                        return self.high < __value.high

        else:
            if type(__value) == Card:
                return False
            else:
                raise TypeError
        



def plural_display_high(string):

    if string in ("ace","two","three","four","five","six","seven","eight","nine","ten","jack","queen","king"):
        if string == "six":
            return "sixes"
        else :
            return string+"s"
    else:
        return None


        
        
        