from socket import *
from Lobby import *
from Player import *


class Main:
    """
        on proggram start
    """

    def __init__(self) -> None:  #initialise les variables principales
        self.lobbys = []
        self.players = []
        self.threads = []

        self.ports = (5567,5568,5569,5570,5571,5572,5573,5574,5575,5576,5577,5578,5579,5580)
        self.next_port_index = 0

    def start(self):   #lance l'écoute serveur et le script
        pass
    
    def listen_connections(self):
        pass
    def on_new_player_connect(self):
        pass

    def redirect_to_lobby(self,lobby : Lobby, player : Player):
        pass

    






def send_packet(packet : str, conn : socket):
    pass

def send_lobbys(conn : socket, lobbys : list):
    pass

def create_lobby(cave : int, is_private : bool):
    try:
        return Lobby(cave,is_private)
    
    except TypeError:
        return False





if __name__ == "__main__":
    main = Main()
    main.start()
