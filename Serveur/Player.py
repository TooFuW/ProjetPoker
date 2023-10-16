from socket import *
from Hand import *

class Player:

    """
      Represent a player who will play a game of poker.
    """

    def __init__(self,id : int, pseudo : str, conn : socket, is_alive : bool, bank : int, address,hand = Hand(),actif : bool = True ,state : str = "ne_peut_pas_parler", connected : bool = True ) -> None:

        if type(id) == int:
            self.id = id
        else:
            print("erreur lors de la création du joueur.")
            raise TypeError
        
        if type(pseudo) == str:
            self.pseudo = pseudo
        else:
            print("erreur lors de la création du joueur.")
            raise TypeError
        
        if type(conn) == socket or conn == None:
            self.conn = conn
        else:
            print("erreur lors de la création du joueur.")
            raise TypeError
        
        if type(is_alive) == bool:
            self.is_alive = is_alive
        else:
            print("erreur lors de la création du joueur.")
            raise TypeError
        
        if type(hand) == Hand:
            self.hand = hand
        else:
            print("erreur lors de la création du joueur.")
            raise TypeError
        if type(bank) == int:
            self.bank = bank
        else:
            print("erreur lors de la création du joueur.")
            raise TypeError
        
        self.address = address
        self.connected = connected

        self.state = state
        #Initialise l'état du joueur
        
        self.chips = 1500
        #print("le joueur a bien été créé")
        

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
    
    def get_chips(self) -> int:
        return self.chips
    
    def get_address(self):
        return self.address
    
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
        if type(conn) == socket:
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
            if self.bank < amount:
                raise ValueError
            if amount >=0:
                self.bank -= amount
            if self.bank < 0:
                self.bank = 0
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
        
    def update_state(self, new_state : str):
        '''Cette fonction permet de changer l'état d'un joueur en un autre'''
        self.state = new_state

    def get_state(self):
        '''Permet d'obtenir l'état d'un joueur'''
        return self.state

    
    


