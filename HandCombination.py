from Combination import Combination
from Card import Card


class HandCombination:
    def __init__(self,hand_combination : list) -> None:
        """_summary_

        Args:
            hand_combination (list): dois etre sous la forme [Combination, Card, Card ...]

        Raises:
            ValueError: ne respecte pas la forme
            ValueError: ne repsecte pas la forme
            TypeError: n'est pas une liste
        """

        if type(hand_combination) == list:
            if [type(el) == Combination for el in hand_combination].count(True) == 1:
                if [type(el) == Card for el in hand_combination].count(True) == len(hand_combination)-1:
                    self.hand_combination = hand_combination
                    self.hand_combination = sorted(self.hand_combination)
                else:
                    raise ValueError
            else:
                raise ValueError
        else:
            raise TypeError
        

    def __str__(self) -> str:
        string = "["
        for el in self.hand_combination:
            string += str(el)+", "
        string = string[0:-2]
        string += "]"
        return string
    

    def __eq__(self, __value: object) -> bool:
        if type(__value) == HandCombination:

            return self.hand_combination == __value.hand_combination
        
        else:
            return False
                

    def __mt__(self, __value : object):

        if type(__value) == HandCombination:

            if self.hand_combination[0] == __value.hand_combination[0]:

                remaining_cards = len(self.hand_combination)-1

                if remaining_cards > 0:

                    for i in range(1,remaining_cards):

                        if self.hand_combination[i] > __value.hand_combination[i]:
                            return True
                        elif self.hand_combination[i] < __value.hand_combination[i]:
                            return False
                        else:
                            pass

                    return False
                            
                else:
                    return False
                
            
            elif self.hand_combination[0] > __value.hand_combination[0]:
                return True
            
            elif self.hand_combination[0] < __value.hand_combination[0]:
                return False
            
    def __lt__(self, __value : object):

         if type(__value) == HandCombination:

            if self.hand_combination[0] == __value.hand_combination[0]:

                remaining_cards = len(self.hand_combination)-1

                if remaining_cards > 0:

                    for i in range(1,remaining_cards):

                        if self.hand_combination[i] > __value.hand_combination[i]:
                            return False
                        elif self.hand_combination[i] < __value.hand_combination[i]:
                            return True
                        else:
                            pass

                    return False
                            
                else:
                    return False
                
            
            elif self.hand_combination[0] > __value.hand_combination[0]:
                return False
            
            elif self.hand_combination[0] < __value.hand_combination[0]:
                return True




                

