from socket import *
from Lobby import *
from Player import *
from threading import *


class Main:
    

    def __init__(self) -> None:  #initialise les variables principales
        self.lobbys = []
        self.players = []
        self.threads = []

        self.lobbys_ports = (5567,5568,5569,5570,5571,5572,5573,5574,5575,5576,5577,5578,5579,5580)
        self.next_port_index = 0

        self.host,self.port = "localhost",5566
        self.server_on = False


    def start(self):   #lance l'écoute serveur et le script
        try:
            self.server_socket = socket(AF_INET, SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"\nServer is listenning for connections on {self.host}:{self.port}")
            self.server_on = True

            while self.server_on:
                self.client_socket, self.client_address = self.server_socket.accept()
                self.on_new_connection(socket=self.client_socket)

        except:
            print("server closed")
    

    def listen_connections(self):
        pass

    def on_new_connection(self,socket : socket,):
        pass

    def redirect_to_lobby(self,lobby : Lobby, player : Player):
        pass

    def close_server(self):
        pass #procédé fermeture serveur
        self.server_on = False


def send_packet(packet : str, conn : socket):
    pass

def send_lobbys(conn : socket, lobbys : list):
    pass

def create_lobby(id : int,cave : int, is_private : bool, host : int, port : int):
    try:
        return Lobby(id,cave,is_private,host,port)
    
    except TypeError:
        return False





if __name__ == "__main__":
    main = Main()
    main.start()
