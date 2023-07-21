from socket import *
from Lobby import *
from Player import *
from threading import *
from sqlite3 import *
from strtotuple import strtotuple
from str_to_list import str_to_list
from random import randint
import sys

a = []
print(sys.getsizeof(a))

class Main:
    

    def __init__(self) -> None:  #initialise les variables principales

        self.lobbys_ports = (5567,5568,5569,5570,5571,5572,5573,5574,5575,5576,5577,5578,5579,5580)
        self.lobbys = [Lobby(randint(100000,999999),"lobby_"+str(i+1),randint(3,10),int(randint(25,1000)*10),False,"localhost",self.lobbys_ports[i]) for i in range(14)]
        print(self.lobbys)
        self.players = []
        self.threads = []

        
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

        except Exception as ex :
            print("server closed", ex)
    

    def handle_client(self,socket : socket, address, id_thread : int):
        connected = True
        print("Etablished connexion with ",address)
        while connected:
            try :
                data = socket.recv(1024)
                data = data.decode("utf8")
                self.manage_data(data,socket )

            except:
                connected = False

        #protocole de déconnexion here

    def manage_data(self,packet : str, socket : socket):
        try:
            data = strtotuple(packet)
            header,body = data[0],data[1]
            
            match header:
                #plein de headers et leur gestion

                case "get_lobbys":
                    lobbys = [lobby for lobby in self.lobbys if type(lobby) == int or (type(lobby) == Lobby and not lobby.is_private)]
                    lobbys = lobbys
                    send_lobbys_public = Thread(target=send_lobbys, args=(socket, lobbys))
                    send_lobbys_public.start()

                case "connect_to_lobby":
                    try :
                        int(body)
                    except:
                        pass # envoi packet error

                case "create_lobby":
                    try:
                        body = str_to_list(body)
                        name,capacityr,cave, is_private = body[0],body[1],body[2],body[3]
                        lobby_ids = [lobby.get_id() for lobby in self.lobbys if type(lobby) == Lobby]

                    except:
                        pass #packet erreur
                    


        except:
            raise TypeError


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
    try:
        conn.send(packet.encode("utf8"))
    except Exception as el:
        print(el)

def send_lobbys(conn : socket, lobbys_display : list):
    print("envoi lobbys",socket)
    lobbys_display = [str(lobby) for lobby in lobbys_display]
    #partie qui prends les infos des lobbys et les range dans la liste sous forme de str
    envoi_packet = Thread(target=send_packet, args=("lobbys="+str(lobbys_display), conn))
    envoi_packet.start()

def create_lobby(id : int,name : str, capacity : int, cave : int, is_private : bool, host : int, port : int):
    try:
        return Lobby(id,name,capacity,cave,is_private,host,port)
    
    except TypeError:
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
