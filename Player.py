from socket import *
from Hand import *

class Player:

    """
      Represent a player who will play a game of poker.
    """

    def __init__(self,id : int, pseudo : str, conn : socket, is_alive : bool, hand : Hand) -> None:

        self.id = id
        self.pseudo = pseudo
        self.conn = conn
        self.is_alive = is_alive
        self.hand = hand

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

    
    


