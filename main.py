from socket import *
from Lobby import *
from Player import *
from threading import *
from sqlite3 import *
from strtotuple import strtotuple


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
                self.on_new_connection(socket=self.client_socket, address=self.client_address)

        except:
            print("server closed")
    

    def handle_client(self,socket : socket, address, id_thread : int):
        connected = True
        print("Etablished connexion with ",address)


    def on_new_connection(self,socket : socket,address):

        id_thread = len(self.threads)
        self.threads.append(Thread(target=self.handle_client, args=(socket,address,id_thread)))
        self.threads[id_thread].start()


    def redirect_to_lobby(self,lobby : Lobby, player : Player):
        pass

    def close_server(self):
        pass #procédé fermeture serveur
        self.server_on = False

    def add_player(self, player : Player):
        if type(player) == Player:
            if True :
                self.players.append()

    def on_deconnect(self,player : Player):
        pass


    def kick(self,conn : socket):
        conn.close()


def send_packet(packet : str, conn : socket):
    pass

def send_lobbys(conn : socket, lobbys : list):
    pass

def create_lobby(id : int,cave : int, is_private : bool, host : int, port : int):
    try:
        return Lobby(id,cave,is_private,host,port)
    
    except TypeError:
        raise TypeError
    
def create_player(id : int, pseudo : str, conn : socket, is_alive : bool, hand : Hand, bank : int):
    try:
        return Player(id,pseudo,conn,is_alive,hand,bank)
    except:
        raise TypeError
    
def set_conn(player : Player, conn : socket):
        try:
            player.set_conn(conn)
        except:
            raise TypeError


def register(username,password):
    """_summary_

    Args:
        username (str): account username
        password (str): account password
    """


def session_id(username):
    # génère un cookie de session et le stocke dans une db
    return #retourne le session id




if __name__ == "__main__":
    main = Main()
    main.start()
