from socket import *
from Lobby import *
from Player import *
from threading import *
from sqlite3 import *
from random import randint
import sys
from packet_separator import packet_separator

a = []
print(sys.getsizeof(a))

class Main:

    def __init__(self) -> None:  #initialise les variables principales

        self.host, self.port = ("localhost",5566)

        self.lobbys_ports = (5567,5568,5569,5570,5571,5572,5573,5574,5575,5576,5577,5578,5579,5580,5581,5582,5583,5584,5585,5586,5587)
        self.lobbys = [Lobby(randint(100000,999999),"lobby_"+str(i+1),randint(3,10),int(randint(25,1000)*10),False,"localhost",self.lobbys_ports[i]) for i in range(14)]
        self.lobby_ids = [lobby.get_id() for lobby in self.lobbys if type(lobby) == Lobby]
        self.port_id = 14
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
            self.server_on = False
    



    def handle_client(self,socket : socket, address, id_thread : int):
        connected = True
        print("Etablished connexion with ",address)
        while connected:
            try :
                data = socket.recv(1024)
                data = data.decode("utf8")
                thread_manage_data = Thread(target=self.manage_data, args=[data,socket,id_thread])
                thread_manage_data.start()

            except Exception as e:
                print("Erreur dans main.handle_client : ",e)
                connected = False

        #protocole de déconnexion here




    def manage_data(self,packet : str, socket : socket, id_thread : int):
        try:
            
            data = packet_separator(packet)
            
            header,body = data[0],data[1]

            print("packet reçu : ", header, "=", body)
            
            match header:
                #plein de headers et leur gestion

                case "get_lobbys":
                    lobbys = [lobby for lobby in self.lobbys if type(lobby) == int or (type(lobby) == Lobby and not lobby.is_private)]
                    send_lobbys_public = Thread(target=send_lobbys, args=(socket, lobbys))
                    send_lobbys_public.start()

                case "join_lobby":
                    try :
                        if body:
                            lobby_existe = int(body.lstrip()) in [lobby.get_id() for lobby in self.lobbys if type(lobby) == Lobby]
                            if lobby_existe:
                                redirect_thread = Thread(target=self.redirect_to_lobby, args=(self.get_lobby_by_id(int(body)), socket))
                                redirect_thread.start()
                            else:
                                error_thread = Thread(target=send_packet, args=[f"404_lobby_not_exist={body.lstrip()}", socket])
                                error_thread.start()
                        else:
                                error_thread = Thread(target=send_packet, args=[f"404_lobby_not_exist={body.lstrip()}", socket])
                                error_thread.start()



                    except:
                        pass # envoi packet error

                case "create_lobby":
                    try:
                        body = eval(body)
                        name,capacity,cave, is_private = body[0],int(body[1]),int(body[2]),eval(body[3])
                        print(body)
                    
                        # conditions vérification paramètres ...
                        new_lobby = self.create_lobby(name,capacity,cave,is_private,"localhost")
                        print("New lobby ! : ", str(new_lobby))
                        self.lobbys.append(new_lobby)
                        lobby_start = Thread(target=self.lobbys[-1].start, args=())
                    
                        

                    except Exception as e:
                        #packet erreur
                        print(e)

                case "get_sits_infos":
                    try:
                        print("requete sur main : get_sits_infos, lobby = "+body)
                        body = body.split(";")

                        lobby_id = int(body[0])
                        func_id = body[1]

                        lobby = self.get_lobby_by_id(lobby_id)
                        thread_send_sits_infos = Thread(target=lobby.send_sits_infos, args=[socket,func_id])
                        thread_send_sits_infos.start()

                    except Exception as e:
                        print("Erreur dans main.get_sits_infos : ", e)

                case "pwd":
                    pwd = "pwd="+"Main;"+self.host+";"+str(self.port)

                    thread_send_pwd = Thread(target=send_packet, args=[pwd,socket])
                    thread_send_pwd.start()


        except:
            raise TypeError


    def on_new_connection(self,socket : socket,address):

        id_thread = len(self.threads)
        self.threads.append(Thread(target=self.handle_client, args=(socket,address,id_thread)))
        self.threads[id_thread].start()


    def redirect_to_lobby(self,lobby : Lobby, conn : socket):
        packet_redirect = "redirect="+str(lobby.host)+":"+str(lobby.port)
        redirect_thread = Thread(target=send_packet,args=(packet_redirect, conn))
        redirect_thread.start()

        conn.close()

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

    def create_lobby(self, name : str, capacity : int, cave : int, is_private : bool, host : str):
        try:
            # conditions vérification paramètres ...
            id_new_lobby = randint(100000,999999)
            while id_new_lobby in self.lobby_ids:
                id_new_lobby = randint(100000,999999)
            self.lobby_ids.append(id_new_lobby)
            return Lobby(id_new_lobby,name,capacity,cave,is_private,host,self.next_lobby_port())
        
        except TypeError:
            raise TypeError
        
    def next_lobby_port(self):
        new_port = self.lobbys_ports[self.port_id]
        self.port_id += 1
        return new_port
    
    def is_listenning(self) -> bool:
        return self.server_on
    
    def get_lobby_by_id(self, id : int):
        try:
            id = int(id)
            for lobby in self.lobbys:
                if lobby.get_id() == id:
                    return lobby
            return
        except:
            raise TypeError



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
