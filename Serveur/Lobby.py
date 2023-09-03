from Player import Player
from socket import *
from Game import Game
from threading import *
from Hand import Hand
from random import randint
from Sit import Sit
from packet_separator import packet_separator
from typing import List


class Lobby :
    """
        Represent a lobby wich listen players on a port and start a game when the lobby is full
        Manage packet interactions in Games

        Sits = liste de sièges pouvant être occupés ou non

    """
    def __init__(self,id : int, name : str,  capacity : int, cave : int, is_private : bool, host : str,port : int) -> None:
        self.players : List[Player] = []
        self.threads : List[Thread] = []
        self.lobby_on = False
        self.is_game_starting = False
        self.players_ids = []
        self.game = None

        self.sits_number = capacity
        self.sits = new_sits(self.sits_number)
        self.sits : List[Sit]

        if type(name) == str and type(capacity) == int and type(cave) == int and type(is_private) == bool and type(host) == str and type(port) == int and type(id) == int:
            self.id = id
            self.cave = cave
            self.is_private = is_private
            self.host, self.port = host,port
            self.name = name
            self.capacity = capacity

        else:
            raise TypeError
        
        self.start() #écoute du lobby
        
    def __str__(self):
        return f"[{self.id}, '{self.name}', {self.capacity},{self.cave}, {self.is_private}, '{self.host}', {self.port}]"
        
    def start(self):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"\nLobby waiting for connections on {self.host}:{self.port}")

        listen_connections = Thread(target=self.listen_connections, args=[])
        
        listen_connections.start()
        

    def handle_client(self,socket : socket, address, id_thread : int):
        connected = True
        print("Etablished connexion with ",address)
        while connected:
            try :
                data = socket.recv(1024)
                data = data.decode("utf8")
                thread_manage_data = Thread(target=self.manage_data, args=[socket,data,id_thread])
                thread_manage_data.start()

            except:
                print("Déconnecté de Lobby n°",self.id)
                connected = False

    def handle_main(self, socket : socket, address, id_thread : int):
        pass
        
    def listen_connections(self):
        self.lobby_on = True
        while self.lobby_on:
            self.client_socket, self.client_address = self.server_socket.accept()
            self.on_new_connection(self.client_socket, self.client_address)
    
    def on_new_connection(self,conn : socket, address):
        id_thread = len(self.threads)
        self.threads.append(Thread(target=self.handle_client, args=(conn,address,id_thread)))

        if not self.socket_in_players(conn): # on ne crée pas 2 players avec la même connexion.
            new_player_thread = Thread(target=self.create_player, args=("dummy",conn,True,1800))  #gestion de bdd pour la bank
            new_player = self.create_player("dummy",conn,True,1800)
            
            self.players.append(new_player)

        self.threads[id_thread].start()
        thread_broadcast = Thread(target=self.broadcast_new_connection, args=[new_player.get_pseudo()])
        thread_broadcast.start()
    

    def manage_data(self, socket : socket, data : str,id_thread : int):
        try:
        
            data = packet_separator(data)
            header,body = data[0],data[1]

            print("packet reçu : ", header, "=", body)

            match header:
                case "get_players_pseudos":
                    packet = "players_pseudos=["
                    for player in self.players:
                        packet += player.get_pseudo()+","
                    packet = packet[0:-1] + "]"

                    if packet == "players_pseudos=[":
                        packet = "player_pseudos=no players in this lobby."

                    envoi_packet_thread = Thread(target=self.send_packet, args=[packet, socket])
                    envoi_packet_thread.start()
                
                case "players_count":
                    nb_joueurs = len(self.players)
                    packet = "players_count="+str(nb_joueurs)
                    envoi_packet_thread = Thread(target=self.send_packet, args=[packet, socket])
                    envoi_packet_thread.start()

                case "get_sits_infos":
                        try:
                            
                            send_sits_infos_thread = Thread(target=self.send_sits_infos, args=[socket])
                            send_sits_infos_thread.start()
                            print("fonction envoi sièges lancées.")
                            

                        except Exception as e:
                            print(e)

                case "sit_down":
                    try:
                        sit_id = int(body)
                        if not sit_id in range(10):
                            raise ValueError
                        
                        sit = self.sits[sit_id]
                        player = self.get_player_by_conn(socket)
                    

                        if not sit.occupied:
                            if not player.sitted:
                                sit.set_player(player)
                                player.sitted = True
                            else:
                                former_sit = self.get_sit_by_player(player)
                                former_sit.remove_player()
                                sit.set_player(player)
                                player.sitted = True
                        
                            self.sits_infos_edited()

                        else:
                            pass
                            # siège occupé

                    except Exception as e:
                        if type(e)==ValueError:
                            print("erreur fonction lobby.sit_down")
                            #packet erreur valeur
                        else :
                            print("erreur fonction lobby.sit_down")


                case "sit_up":
                    player = self.get_player_by_conn(socket)
                    sit = self.get_sit_by_player(player)
                    self.sits_infos_edited()
        
                    if sit is None:
                        # Le joueur n'est assis nulle part
                        pass
                    else:
                        sit.remove_player()
                            
                case "start_game":
                    print(id(self.sits))
                    self.init_game()
                    self.start_game()
                    self.sits[0].set_player(self.players[0])
                    print(self.sits[0])
                    self.game.print_sits()
                case "pwd":
                    pwd = "pwd=Lobby "+str(self.id)+";"+self.host+";"+str(self.port)

                    thread_send_pwd = Thread(target=self.send_packet, args=[pwd,socket])
                    thread_send_pwd.start()


                case "go_main":
                    # on lance le packet de redirection puis on ferme le socket actuel et on supprime le thread d'écoute des threads
                    thread_redirect_main = Thread(target=self.send_packet, args=["redirect=localhost:5566",socket])
                    thread_redirect_main.start()

                    socket.close()
                    

                case "threads":
                    print(len(self.threads), self.threads)


        except Exception as e:
            print("Erreur dans Lobby.manage_data : ",e)




                

    def send_packet(self, packet : str, conn : socket):
        try:
            conn.send(packet.encode("utf8"))
        except Exception as el:
            print(el)


    def create_player(self,pseudo : str, conn : socket, is_alive : bool, bank : int, hand = None):

        newid = randint(100000,999999)
        while newid in self.players_ids:
            newid = randint(100000,999999)
        self.players_ids.append(newid)

        try:
            if not hand is None:
                print("le player est sur le point d'etre créé.")
                player  = Player(newid,pseudo,conn,is_alive,bank,hand)
                print(player)
                return player
            else:
                print("le player est sur le point d'etre créé.")
                player = Player(newid,pseudo,conn,is_alive,bank)
                print(player)
                return player

        except:
            print("erreur lors de la création du player.")
            raise TypeError
        
    if False:
        def main_connect(self):

            self.main_socket = socket(AF_INET, SOCK_STREAM)
            self.main_socket.connect(("localhost", 5566))
            
    
    def init_game(self):
        if not self.is_game_starting:
            self.game = Game(self.sits, self.cave)

    def start_game(self):
        self.is_game_starting = True
        # envoie packet game entrain de commencer
        # compteur 5 secondes
        self.game.start()

    def edit_game_sits(self):
        pass

    def get_sit_by_id(self,id_sit) -> Sit:
        for sit in self.sits:
            if sit.get_id() == id_sit:
                return sit
    
    def get_sit_by_player(self, player) -> Sit:
        for sit in self.sits:
            if sit.get_player() == player:
                return sit
            
    def get_player_by_conn(self,conn : socket) -> Player:
        try :

            for pl in self.players:
                if pl.get_conn() == conn:
                    return pl
            return None
        
        except Exception as e:
            print("erreur fonction lobby.get_player_by_conn : " , e)

            
    def check_is_connected(self, player : Player):
        """ Vérifie si un joueur est encore connecté au lobby

        Args:
            player (Player): Player de qui on veut vérifier la présence
        """
        # on envoie un paquet de demande de réponse avec calcul simple, on attends une réponse, si on obtient pas la réponse attendue le joueur est considéré deconnecté 
        pass

    def add_player(self,player : Player):
        pass

    def end_lobby(self):
        pass

    def redirect_all_to_main(players : Player):
        pass
    
    def redirect_player_to_main(self):
        pass

    def broadcast_new_connection(self,pseudo):
        conns = [player.get_conn() for player in self.players]
        for conn in conns:
            packet = "new_player_joined=" + pseudo
            thread_new_player = Thread(target=self.send_packet, args=[packet,conn])
            thread_new_player.start()
            thread_new_player.join()
            print("packet broadcast envoyé.")

    def send_sits_infos(self, conn : socket):
        try:
            sits_infos = []
            for sit in self.sits:
                sit_infos = []
                sit_infos.append(sit.get_sit_id())
                if not sit.occupied:
                    sit_infos.append(None)
                    sits_infos.append(sit_infos)
                    continue

                sit_infos.append("'"+str(sit.get_player().get_pseudo())+"'")
                sit_infos.append(sit.get_player().get_chips())
                sit_infos.append("link to player account")

                sits_infos.append(sit_infos)

            sits_infos = str(sits_infos)
            packet = "sits_infos="+sits_infos

            thread_packet_send = Thread(target=self.send_packet, args=(packet,conn))
            thread_packet_send.start()

        except Exception as e:
            print(e)



    def see_connected_players(self):
        pass

    def get_id(self):
        copy = self.id
        return copy    

    def is_listenning(self):
        return self.lobby_on

    def socket_in_players(self,conn : socket):
        if type(conn) == socket:
            return conn in [player.get_conn() for player in self.players]
        
    def sits_infos_edited(self):
        for pl in self.players:
            conn = pl.get_conn()
            thread_send_sits_infos = Thread(target=self.send_sits_infos, args=[conn])
            thread_send_sits_infos.start()

        
    def force_stop(self):
        """En cas de demande de fermeture forcée. 
        Enclenche la fermeture forcée de la game en cours avant de déconnecter de force tous les joueurs puis s'eteindre.
        """
        pass


def new_sits(n : int):
    sits = []
    for i in range(n):
        sit = Sit(i)
        sits.append(sit)
    return sits


def on_player_deconnect(player : Player):
    pass


if __name__ == "__main__":
    pass