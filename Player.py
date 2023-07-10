from socket import *
from Hand import *

class Player:

    """
      Represent a player who will play a game of poker.
    """

    def __init__(self,id : int, pseudo : str, conn : socket, is_alive : bool, hand : Hand) -> None:

        if type(id) == int:
            self.id = id
        else:
            raise TypeError
        
        if type(pseudo) == str:
            self.pseudo = pseudo
        else:
            raise TypeError
        
        if type(conn) == socket:
            self.conn = conn
        else:
            raise TypeError
        
        if type(is_alive) == bool:
            self.is_alive = is_alive
        else:
            raise TypeError
        
        if type(hand) == Hand:
            self.hand = hand
        else:
            raise TypeError
        

    def __str__(self) -> str:
        string = ""


    def get_id(self) -> int:
        return self.id
    
    def get_pseudo(self) -> str:
        return self.get_pseudo
    
    def get_conn(self) -> socket:
        return self.conn
    
    def get_hand(self) -> Hand:
        return self.hand
    
    def edit_pseudo(self, pseudo : str):
        self.pseudo = pseudo
    
    def send_packet(self, packet : str):
        self.conn.send(packet.encode("utf8"))
    
    def set_hand(self,hand : Hand):
        if type(hand) == Hand:
            self.hand = hand
        else :
            raise TypeError
        
    def clear_hand(self):
        self.hand.clear_hand()

    
    


