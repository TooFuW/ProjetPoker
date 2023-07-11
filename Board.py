import Card
import AlreadyExistingCard

class Board :
    """
        Represent the board of card visible by all

    """

    def __init__(self, board : list) -> None:
        
        if type(board) == list:
            if only_cards(board):
                self.board = board
            else:
                raise AlreadyExistingCard
        else:
            raise TypeError




    def __str__(self) -> str:

        string = "["
        for i in self.board:
            string += str(i)+", "
        string = string[0:-2]
        string += "]"

        return string
    
    def get_board(self) -> list:
        return self.board.copy()

    
    def add_card(self,card : Card):

        if card in self.board :
            raise AlreadyExistingCard(card)
        
        elif type(card) != Card:
            raise TypeError
        
        else:
            self.board.append(card)


    def clear_board(self):
        self.board = []


    def pop_card(self):

        if self.board == []:
            pass
        else:
            self.board.remove(self.board[0])

    
    def remove_card(self,card : Card):

        if not card in self.board:
            raise ValueError
        else:
            self.board.remove(card)


def only_cards(liste):
    if liste == []:
        return True
    
    for i in liste:
        if type(i) != Card:
            return False
    return True

