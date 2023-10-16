from Player import Player
from socket import *
from Game import Game
from threading import *
from Hand import Hand
from random import randint
from Sit import Sit
from packet_separator import packet_separator
from typing import List
import time
from Log import *
from Pot import Pot


class Lobby :
    """
        Represent a lobby wich listen players on a port and start a game when the lobby is full
        Manage packet interactions in Games

        Sits = liste de sièges pouvant être occupés ou non

    """
    def __init__(self,id : int, name : str,  capacity : int, cave : int, is_private : bool, host : str,port : int) -> None:

        self.players : List[Player] = []
        self.threads : List[Thread] = []
        self.pots : List[Pot] = []
        self.lobby_on = False
        self.is_game_starting = False
        self.players_ids = []
        self.game : Game = None
        self.is_continue_timer = False
        self.timer_running = False

        self.sits_number = capacity
        self.sits = new_sits(self.sits_number)
        self.sits : List[Sit]

        self.func_id_dict = {}

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
        
    def __str__(self) -> str:
        return f"[{self.id}, '{self.name}', {self.capacity},{self.cave}, {self.is_private}, '{self.host}', {self.port}]"
        
    def start(self):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"\nLobby waiting for connections on {self.host}:{self.port}")

        listen_connections = Thread(target=self.listen_connections, args=[])
        #listen_state = Thread(target=self.listen_state)
        
        listen_connections.start()
        #listen_state.start()

    
    

    def new_func_id_dict_number(self) -> int:
        """Renvoie une nouvelle clé pour func_id_dict

        on prends un nombre aléatoire à 6 chiffres qui n'est pas déja une clé.

        Returns:
            int: la nouvelle clé
        """
   
        nb = randint(100000, 999999)
        while nb in self.func_id_dict.keys(): 
            nb = randint(100000, 999999)
        return nb

    def add_func_id_dict(self,key,value):
        self.func_id_dict[key] = value

    def func_id_dict_object_by_key(self,key):
        return self.func_id_dict[key]

    def delete_func_id_dict_key(self,key):
        del self.func_id_dict[key]




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
        """s'execute à l'acceptation d'un socket

        Args:
            conn (socket): _description_
            address (_type_): _description_
        """

        if is_ip_in_blacklist(address[0]):

            self.refuse_connection(conn, address)

        else:    

            id_thread = len(self.threads)
            self.threads.append(Thread(target=self.handle_client, args=(conn,address,id_thread)))

            if not self.address_in_players(address): # on ne crée pas 2 players avec la même connexion ou la même adresse.
                #gestion de bdd pour la bank
                print("new player, address : ",address)
                new_player = self.create_player("dummy",conn,True,1800,address=address)

            else :
                print("suii")
                new_player = self.get_player_by_address(address)
                new_player.set_conn(conn)

            write_lobby_connexion(address, self.id,True)

            

            thread_check_connection = Thread(target=self.check_connection, args=[conn])
            self.players.append(new_player)

            self.threads[id_thread].start()
            thread_broadcast = Thread(target=self.broadcast_new_connection, args=[new_player.get_pseudo()])
            thread_broadcast.start()
            thread_check_connection.start()


    def handshake(self,conn : socket):

        func_id = self.new_func_id_dict_number()
        self.add_func_id_dict(func_id,None)
        message = "handshake="+str(func_id)

        shake_result = self.func_id_dict_object_by_key(func_id)
        cpt = 0

        thread_send_handshake = Thread(target=self.send_packet, args=(message,conn))
        thread_send_handshake.start()

        while (shake_result is None and cpt < 5 ) or cpt == 0:
            shake_result = self.func_id_dict_object_by_key(func_id)
            time.sleep(0.2)
            cpt += 1

        self.delete_func_id_dict_key(func_id)
        return shake_result



    def check_connection(self,conn : socket):
        """Envoie des handshake pour vérifier la présence de chaque connexion. 
        en cas d'échec il entreprends le protocole de deconnexion du joueur.

        Args:
            conn (socket): _description_
        """

        print("Lancement check connection",conn)
        failed_handshake_row = 0

        while failed_handshake_row < 3:
            current_handshake = self.handshake(conn)

            if current_handshake is None:
                failed_handshake_row += 1 # un handshake a echoué.
                print("handshake échoué.")

            if current_handshake:
                failed_handshake_row = 0 # le handshake a réussi.
                
            else:
                failed_handshake_row += 1 # ???

        print(conn," DECONNECTE")

        pl = self.get_player_by_conn(conn)

        if not pl is None:
            print("protocole de deconnexion") 
            self.on_player_deconnect(pl)  # PROTOCOLE DE DECONNEXION
            
        else:
            print("aucun joueur associé à ce socket : ",conn)


    

    def manage_data(self, socket : socket, data : str,id_thread : int):
        try :
        
            data = packet_separator(data)
            header,body = data[0],data[1]

            if not header == "handshake":
                print("packet reçu : ", header, "=", body)

            match header:

                case "handshake":
                    try:
                        func_id = int(body)

                        self.func_id_dict[func_id] = True   # on essaie de rendre le paquet bien reçu.


                    except:
                        print("erreur dans Lobby.manage_data case handshake") # le paquet n'a pas été reçu ou est erroné. handshake echoué.




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
                            
                            body = body.split(";")

                            send_sits_infos_thread = Thread(target=self.send_sits_infos, args=(socket, body[1]))
                            send_sits_infos_thread.start()
                            print("fonction envoi sièges lancées.")
                            

                        except Exception as e:
                            print(e)

                case "sit_down":
                    try:

                        sit_id = int(body)

                        if not sit_id in range(10):
                            print("siege n'existe pas")
                        
                        sit = self.sits[sit_id]
                        player = self.get_player_by_conn(socket)
                        former_sit = self.get_sit_by_player(player)

                        if not sit.occupied:

                            if former_sit is None:
                                sit.set_player(player)
                                
                            else:
                                former_sit.remove_player()
                                sit.set_player(player)
                               
                        
                            self.sits_infos_edited()


                        else:
                            print("siege occupé")
                            # siège occupé

                    except Exception as e:
                        if type(e)==ValueError:
                            print("erreur fonction lobby.sit_down")
                            #packet erreur valeur
                        else :
                            print("erreur fonction lobby.sit_down",e)


                case "sit_up":
                    self.sit_up(socket)
                     ########### TEST GAME ###########
                            
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



        except Exception as e :
            print("Erreur dans Lobby.manage_data : ",e)




                

    def send_packet(self, packet : str, conn : socket):
        try:
            conn.send(packet.encode("utf8"))
        except Exception as el:
            print(el)


    def broadcast_packet(self,packet : str):
        for pl in self.players:
            thread_send_packet = Thread(target=self.send_packet, args=(packet,pl.get_conn()))
            thread_send_packet.start()


    def check_players_state(self):
        func_timer_id = self.new_func_id_dict_number()
      

        count = 0
        for sit in self.sits:
            sit_pl = sit.get_player()
            if not sit_pl is None:
                if sit_pl.connected:
                    count += 1

        if count >= 2:
            self.add_func_id_dict(func_timer_id, True)
            
            thread_timer = Thread(target=self.start_timer, args=[func_timer_id])
            thread_timer.start()

        else:
            self.add_func_id_dict(func_timer_id, False)






    def sit_up(self,conn):
        player = self.get_player_by_conn(conn)
        sit = self.get_sit_by_player(player)
        

        if sit is None:
            
            # Le joueur n'est assis nulle part
            pass
        else:
         
            sit.remove_player()

            self.sits_infos_edited() # on édite seulement s'il se produit un changement.

        
    def start_timer (self):
        
        timer = 20
        if not self.timer_running:

            self.timer_running = True

            thread_start_timer = Thread(target=self.broadcast_packet,args=['start_timer=20'])
            thread_start_timer.start()

            while timer > 0 and self.is_continue_timer:
                
                if len([pl.get_player() for pl in self.sits if pl.get_player() != None]) >= 2:

                    time.sleep(1)
                    timer -= 1
                    print(timer)

                else:

                    self.is_continue_timer = False

            self.timer_running = False

            if self.is_continue_timer:
                print("GAME COMMENCE")  # PROTOCOLE LANCEMENT DE GAME 
            else:
                print("timer arreté")
                thread_start_timer = Thread(target=self.broadcast_packet,args=['stop_timer='])
                thread_start_timer.start()


        else:
            print("le timer est déja lancé ailleurs")# le timer est déja lancé ailleurs

    def stop_timer(self):
        self.is_continue_timer = False


    def create_player(self,pseudo : str, conn : socket, is_alive : bool, bank : int, address, hand = None):

        newid = randint(100000,999999)
        while newid in self.players_ids:
            newid = randint(100000,999999)
        self.players_ids.append(newid)

        try:
            if not hand is None:
                print("le player est sur le point d'etre créé.")
                player  = Player(newid,pseudo,conn,is_alive,bank,hand,address=address)
                print(player)
                return player
            else:
                print("le player est sur le point d'etre créé.")
                player = Player(newid,pseudo,conn,is_alive,bank,address=address)
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
            if not self.is_game_started():
                self.game = Game(self.sits, self.cave, self.players)
            else:
                print("Une game est déjà en cours.")

        else:
            print("une game est entrain d'être démarée")

    def start_game(self):
        self.is_game_starting = True
        # envoie packet game entrain de commencer
        # compteur 5 secondes
        self.game.start()

    # les fonctions qui permettent de savoir si une game, un round, un step est demmaré.

    def is_game_started(self) -> bool:
        """Retourne vrai si la game du lobby est lancée.

        Returns:
            bool: self.game est démarrée ?
        """

        if self.game is None:
            return False
        
        elif isinstance(self.game,Game):
            return self.game.started
        
        else:
            raise ValueError # self.game doit etre None ou une Game.
        

    def is_round_started(self) -> bool:
        """Retourne vrai s'il y a un round lancé dans une game lancée.

        Returns:
            bool: self.game.round pas None et démarée
        """

        if self.is_game_started():
            if not self.game.round is None:
                return self.game.round.started
            
        return False
    
    def is_step_started(self) -> bool:
        """Retourne vrai s'il y a un step lancé dans un round lancé.

        Returns:
            bool: self.game.round.step pas None est demmaré.
        """
        if self.is_round_started():
            if not self.game.round.step is None:
                return self.game.round.step.started
            
        return False
    

    def is_game_initied(self) -> bool:
        """Retourne vrai si la game du lobby est initiée (affectée à une variable).

        Returns:
            bool: self.game est démarrée ?
        """

        if self.game is None:
            return False
        
        elif isinstance(self.game,Game):
            return True
        
        else:
            raise ValueError # self.game doit etre None ou une Game.
        

        
    def is_round_initied(self) -> bool:
        """Retourne vrai s'il y a un round initié dans une game lancée.

        Returns:
            bool: self.game.round pas None
        """

        if self.is_game_started():
            if self.game.round is None:
                return False
            return True
            
        return False
    

    def is_step_initied(self) -> bool:
        """Retourne vrai s'il y a un step initié dans un round lancé.

        Returns:
            bool: self.game.round.step pas None est demmaré.
        """
        if self.is_round_started():
            if self.game.round.step is None:
                return False
            return True
            
        return False
    


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


    def get_player_by_address(self,address):
        try :

            for pl in self.players:
                if pl.get_address() == address:
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

    def send_sits_infos(self, conn : socket, func_id : str = ""):
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

            sits_infos = str(sits_infos)+";"+func_id
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
        
    def address_in_players(self,address):
        return address in [player.get_address() for player in self.players]
        
    def sits_infos_edited(self):
        
        if not self.timer_running:
            print("protocole timer") # on applique le protocole du timer
            self.timer_protocol()
        else:
            print("timer already running")

        for pl in self.players:
            conn = pl.get_conn()
            thread_send_sits_infos = Thread(target=self.send_sits_infos, args=[conn])
            thread_send_sits_infos.start()

        
    def force_stop(self):
        """En cas de demande de fermeture forcée. 
        Enclenche la fermeture forcée de la game en cours avant de déconnecter de force tous les joueurs puis s'eteindre.
        """
        pass

    def refuse_connection(self,conn : socket,address):
        packet = "refused-connection=Connection Refused."
        thread_refuse_connection_packet = Thread(target=self.send_packet, args=(packet,conn))
        thread_refuse_connection_packet.start()
        conn.close()
        write_refused_connection(address)

    def timer_protocol(self):
        if len([pl.get_player() for pl in self.sits if pl.get_player() != None]) >= 2: # on regarde si au moins 2 joueurs assis
            print("le timer peut commencer")
            self.is_continue_timer = True
            thread_timer = Thread(target=self.start_timer)
            thread_timer.start()

        else:
            print("pas assez de joueurs pour commencer")
            self.is_continue_timer = False


    def on_player_deconnect(self,player : Player):
        print("deconnexion de : ",player)
        

        player.connected = False # on set le joueur en deconnecté.
        
        if not self.is_round_initied():
            print("on lève le player : ",player)
            self.sit_up(player.get_conn()) #si aucun round n'est lancé, on lève le joueur.

        else:
            print("round started.")


        try:
            self.players.remove(player) # on le supprime de la liste des joueurs 
        except:
            print("joueur deconnecté pas dans self.players")

        print(self.players)
        


def new_sits(n : int):
    sits = []
    for i in range(n):
        sit = Sit(i)
        sits.append(sit)
    return sits


if __name__ == "__main__":
    pass