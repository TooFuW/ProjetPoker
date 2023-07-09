import Card

class Board :
    """
        Represent the board of card visible by all

    """

    def __init__(self, board : list) -> None:

        self.board = board

    def __str__(self) -> str:

        string = "["
        for i in self.board:
            string += str(i)+", "
        string = string[0:-2]
        string += "]"

        return string
    
    def add_card(self,card : Card):
        pass