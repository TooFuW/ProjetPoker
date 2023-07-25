from socket import *
from Hand import *

class Player:

    """
      Represent a player who will play a game of poker.
    """

    def __init__(self,id : int, pseudo : str, conn : socket, is_alive : bool, bank : int, hand = Hand()) -> None:

        if type(id) == int:
            self.id = id
        else:
            raise TypeError
        
        if type(pseudo) == str:
            self.pseudo = pseudo
        else:
            raise TypeError
        
        if type(conn) == socket or conn == None:
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
        if type(bank) == int:
            self.bank = bank
        else:
            raise TypeError
        
        self.chips = 0
        

    def __str__(self) -> str:
        return f"[Player id : {self.id}, Pseudo : {self.pseudo}, Connection : {self.conn}]"


    def get_id(self) -> int:
        return self.id
    
    def get_pseudo(self) -> str:
        clone = ""
        clone += self.pseudo
        return clone
    
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
        
    def set_conn(self, conn : socket):
        if type(conn) == conn:
            self.conn = conn
        else:
            raise TypeError
        
    def clear_hand(self):
        self.hand.clear_hand()

    def add_card(self,card : Card):
        try:
            self.hand.add_card(card)
        except:
            return False
        
    def bank_remove(self, amount : int):
        if type(amount) == int:
            if amount >=0:
                self.bank -= amount
                #completer avec gestion de base de données
            else:
                raise ValueError
        else:
            raise TypeError

        
    def bank_add(self,amount : int):
        if type(amount) == int:
            if amount >=0:
                self.bank += amount
                #completer avec gestion de base de données
            else:
                raise ValueError
        else:
            raise TypeError

    
    


