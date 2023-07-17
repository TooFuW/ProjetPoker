from Player import Player
from socket import *
from Game import Game

class Lobby :
    """
        Represent a lobby wich listen players on a port and start a game when the lobby is full
        Manage packet interactions in Games

    """
    def __init__(self,cave : int, is_private : bool) -> None:
        self.players = []

        if type(cave) == int and type(is_private) == bool:
            self.cave = cave
            self.is_private = is_private

        else:
            raise TypeError

    def listen_player(self,player : Player):
        pass

    def listen_connections(self):
        pass

    def on_new_connection(self):
        pass
    
    def send_packet(self,packet):
        pass
    

    def add_player(self,player : Player):
        pass

    def end_lobby(self):
        pass

    def redirect_all_to_main(players : Player):
        pass
    
    def redirect_player_to_main(self):
        pass

    def broadcast_new_connection(self):
        pass

    def see_connected_players(self):
        pass


def on_player_deconnect(player : Player):
    pass