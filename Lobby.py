from Player import Player
from socket import *
from Game import Game
from threading import *
from Hand import Hand
from random import randint

class Lobby :
    """
        Represent a lobby wich listen players on a port and start a game when the lobby is full
        Manage packet interactions in Games

    """
    def __init__(self,id : int, name : str,  capacity : int, cave : int, is_private : bool, host : str,port : int) -> None:
        self.players = []
        self.threads = []
        self.lobby_on = False
        self.players_ids = []

        if type(name) == str and type(capacity) == int and type(cave) == int and type(is_private) == bool and type(host) == str and type(port) == int and type(id) == int:
            self.id = id
            self.cave = cave
            self.is_private = is_private
            self.host, self.port = host,port
            self.name = name
            self.capacity = capacity

        else:
            raise TypeError
        
        self.start()
        
    def __str__(self):
        return f"[{self.id}, {self.name}, {self.capacity},{self.cave}, {self.is_private}, {self.host}, {self.port}]"
        
    def start(self):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"\nLobby waiting for connections on {self.host}:{self.port}")

        listen_connections = Thread(target=self.listen_connections, args=[])
        
        listen_connections.start()
        

    def handle_client(self,socket : socket, address, id_thread :  int):
        connected = True
        print("Etablished connexion with ",address)
        while connected:
            try :
                data = socket.recv(1024)
                data = data.decode("utf8")
                self.manage_data(data,socket )

            except:
                connected = False

    def handle_main(self, socket : socket, address, id_thread : int):
        pass
        
    def listen_connections(self):
        self.lobby_on = True
        while self.lobby_on:
            self.client_socket, self.client_address = self.server_socket.accept()
            self.on_new_connection(socket=self.client_socket)
    
    def on_new_connection(self,socket : socket, address):
        id_thread = len(self.threads)
        self.threads.append(Thread(target=self.handle_client, args=(socket,address,id_thread)))
        self.threads[id_thread].start()
    
    def manage_data(self, socket : socket, data : str):
        pass

    def send_packet(self,packet):
        pass


    def create_player(self,pseudo : str, conn : socket, is_alive : bool, hand : Hand, bank : int):
        newid = randint(100000,999999)
        while newid in self.players_ids:
            newid = randint(100000,999999)
        self.players_ids.append(newid)
        try:
            return Player(newid,pseudo,conn,is_alive,hand,bank)
        except:
            raise TypeError    

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

    def get_id(self):
        copy = self.id
        return copy    

    def is_listenning(self):
        return self.lobby_on


def on_player_deconnect(player : Player):
    pass