from Player import *

class Sit :
    
    def __init__(self,sit_id : int = 0 ) -> None:
        """ Représente un siège qui peut être positionné de 0 à 9  et contenir ou nom une personne

        Args:
            id (int, optional): _description_. Defaults to 0.

        set_player quand un joueur s'assois sur le siège
        remove_player quand un joueur se lève

        """

        if sit_id in range(10):
            self.sit_id = sit_id
        else:
            raise ValueError
        
        self.player = None
        self.playerid = None
        self.occupied = False

    def get_player(self):
        return self.player
    
    def get_player_id(self):
        return self.playerid
    

    def set_player(self,player : Player):

        if type(player) == Player:

            self.player = player
            self.playerid = player.get_id()
            self.occupied = True

        else:
            raise TypeError
        
    def remove_player(self):

        self.player = None
        self.playerid = None
        self.occupied = False

    def set_sit_id(self,sit_id):
        if sit_id in range(10):
            self.sit_id = sit_id

    def get_sit_id(self):
        return self.sit_id

       

        