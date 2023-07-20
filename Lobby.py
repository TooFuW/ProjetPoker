from Player import Player
from socket import *
from Game import Game
from threading import *
from Hand import Hand

class Lobby :
    """
        Represent a lobby wich listen players on a port and start a game when the lobby is full
        Manage packet interactions in Games

    """
    def __init__(self,id : int, name : str,  capacity : int, cave : int, is_private : bool, host : int,port : int) -> None:
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
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"\nLobby waiting for connections on {self.host}:{self.port}")

        listen_connections = Thread(target=self.listen_connections, args=[])
        
        listen_connections.start()
        

    def listen_player(self,player : Player):
        pass
        
    def listen_connections(self):
        while self.lobby_on:
            self.client_socket, self.client_address = self.server_socket.accept()
            self.on_new_connection(socket=self.client_socket)

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

def create_player(id : int, pseudo : str, conn : socket, is_alive : bool, hand : Hand, bank : int):
    try:
        return Player(id,pseudo,conn,is_alive,hand,bank)
    except:
        raise TypeError