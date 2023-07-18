from Player import Player
from socket import *
from Game import Game
from threading import *

class Lobby :
    """
        Represent a lobby wich listen players on a port and start a game when the lobby is full
        Manage packet interactions in Games

    """
    def __init__(self,id : int,cave : int, is_private : bool, host : int,port : int) -> None:
        self.players = []
        self.lobby_on = False

        if type(cave) == int and type(is_private) == bool and type(host) == int and type(port) == int and type(id) == int:
            self.id = id
            self.cave = cave
            self.is_private = is_private
            self.host, self.port = host,port

        else:
            raise TypeError
        
    def start(self):
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"\nLobby waiting for connections on {self.host}:{self.port}")

        listen_connections = Thread(target=self.listen_connections, args=[])
        
        listen_connections.start()
        

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