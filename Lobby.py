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

    def add_player(self,player : Player):
        pass


def on_player_deconnect(player : Player):
    pass