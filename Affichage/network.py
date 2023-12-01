"""Document contenant toutes les fonctions permettant de lier le client au serveur"""


from socket import *
from threading import *
from packet_separator import *
from random import *
import Global_objects
import time
from datetime import datetime
from icecream import ic

print(datetime.utcnow())
host, port = ('localhost', 5566)

stop_sending_event = Event()
stop_listenning_event = Event()

listenning_thread = None
sending_thread = None

def send_packet(conn : socket, packet : str) -> None:
    """Envoie un paquet de donnée au client ciblé

    Args:
        conn (socket): objet socket à qui envoyer la paquet
        packet (str): le paquet à envoyer
        
    """
    try :
        conn.send(packet.encode("utf8"))
    except Exception as e:
        print(" Erreur dans network.send_packet : ",e)




def new_func_id_dict_number() -> int:
    """Renvoie une nouvelle clé pour func_id_dict

    on prends un nombre aléatoire à 6 chiffres qui n'est pas déja une clé.

    Returns:
        int: la nouvelle clé
    """
   
    nb = randint(100000, 999999)
    while nb in Global_objects.func_id_dict.keys(): 
        nb = randint(100000, 999999)
    return nb

def add_func_id_dict(key,value):
    Global_objects.func_id_dict[key] = value

def func_id_dict_object_by_key(key):
    return Global_objects.func_id_dict[key]

def delete_func_id_dict_key(key):
    del Global_objects.func_id_dict[key]





def ask_lobbys(client_socket):
    """Demande les lobbys au serveur

    Args:
        client_socket socket : socket du serveur à qui demander
    """

    thread_ask_lobbys = Thread(target=send_packet, args=(client_socket, "get_lobbys="))
    thread_ask_lobbys.start()


def ask_sits_infos(client_socket : socket, lobby_id : int):
    """Demande les infos de sièges d'un lobby

    Args:
        client_socket (socket): le socket à qui demander les lobbys
        lobby_id (int): le lobby dont on veut connaitre les sièges
    """
    try : 
        func_id = new_func_id_dict_number()
        add_func_id_dict(func_id,None)
        sits = func_id_dict_object_by_key(func_id)

        print("ask_sits_infos déclenché")
        message = "get_sits_infos="+str(lobby_id)+";"+str(func_id)

        thread_ask_sits = Thread(target=send_packet, args=(client_socket, message))
        thread_ask_sits.start()

        cpt = 0

        while sits is None and cpt < 10:
            sits = func_id_dict_object_by_key(func_id)
            cpt += 1
            time.sleep(0.01)

        delete_func_id_dict_key(func_id)
        return sits
            


    except Exception as e :
        print("Erreur network.ask_sits_infos : ", e)


def join_lobby(conn : socket, lobby_id : int):
    try:
        message = "join_lobby="+str(lobby_id)

        thread_join_lobby = Thread(target=send_packet, args=(conn,message))
        thread_join_lobby.start()


    except Exception as e:
        print("Erreur dans network.join_lobby : ",e)


def go_main(conn : socket):
    try:
        message = "go_main="

        thread_join_lobby = Thread(target=send_packet, args=(conn,message))
        thread_join_lobby.start()

    except Exception as e:
        print("Erreur dans network.join_lobby : ",e)






def sit_down(client_socket : socket, sit_id : int):
    try:
        message = "sit_down="+str(sit_id)
        
        thread_sit_down = Thread(target=send_packet, args=(client_socket,message))
        thread_sit_down.start()


    except Exception as e:
        print("Erreur network.sit_down : ",e)

def sit_up(client_socket : socket):
    try:
        message = "sit_up="
        
        thread_sit_up = Thread(target=send_packet, args=(client_socket,message))
        thread_sit_up.start()
        


    except Exception as e:
        print("Erreur network.sit_down : ",e)

def recieve_data(conn : socket):
    connecte = True
    print("Écoute des paquets sur : ",conn)

    while connecte:
        if stop_listenning_event.is_set():
            print("fin d'écoute sur ",conn)
            break
        try:
            data = conn.recv(1024)
            data = data.decode("utf-8")

            thread_manage_data = Thread(target=manage_data, args=[conn,data])
            thread_manage_data.start()

        except Exception as e:
            print("Erreur sur network.recieve_data : ",e)
            connecte = False
            break

    print("fin d'écoute sur ",conn)




def check_lobby_exist(conn : socket, lobby_id : int):
    """Demande au serveur si un numéro de lobby spécifié existe.
       3 réponses possibles : True, False, None si le serveur n'a pas de réponse 

       Pour cela il sera indispensable de pouvoir modifier des variables à l'aide des pointeurs !

    Args:
        conn (socket): _description_
        lobby_id (int): _description_
    """
    thread_ask_packet = Thread(target=send_packet, args=[])
    pass

def connect_to_lobby(conn : socket, lobby_id : int):
    pass

def manage_data(conn : socket, packet : str):
    try : 
        packet = packet_separator(packet)

        entete = packet[0]
        body = packet[1]

        if entete!= "handshake":
            print(packet)

        del packet

        match entete:

            case "lobbys": # Récéption des lobbys
                try:
                        # Traitement des lobbys puis enregistrement dans la variable globale correspondante
                        lobbys = eval(body)  

                        for i in range(len(lobbys)):
                            lobbys[i] = eval(lobbys[i])
                            print(lobbys[i], type(lobbys[i]))
                            
                        Global_objects.lobbys_list = lobbys
                        
                        edit_displayed_lobbys_list(lobbys)

                except Exception as e:
                    print("Erreur dans network.manage_data case lobbys : ",e)

            case "sits_infos":
                    try:
                        print(body)
                        body = body.split(";")
                        func_id = body[1] # on récupère la func_id

                        body = eval(body[0]) # on transforme la chaine de caractères en liste de chaines de caractères

                        # on trasforme chaque str dans body en liste
                        for i in range(len(body)):
                            if type(body) == str:
                                body[i] = eval(body[i])

                        # on appelle la fonction de gestion de données, si une func_id est précisée ou non
                        if func_id == "":
                            recieve_sits_infos(body)
                        else:
                            recieve_sits_infos(body,int(func_id))


                    except Exception as e:
                        print("Erreur sur réception paquet sits_infos : ",e)


            case "redirect":
                try:
                    global listenning_thread
                    print("redirection...")

                    body = body.split(":")
                    host,port = body[0],int(body[1])
                    # fermeture de l'ancien socket
                    stop_listenning(listenning_thread)
                    Global_objects.client_socket.close()
                    # création du socket lobby
                    client_socket_lobby = socket(AF_INET, SOCK_STREAM)
                    

                    # attribution du nouveau socket à la variable globale
                    client_socket_lobby.connect((host, port))

                    Global_objects.client_socket = client_socket_lobby

                    print("Connecté au lobby.", host, port)

        
                    start_listenning(Global_objects.client_socket)
                        # a suivre ...

                    
                except:
                    print("Erreur network.manage_data case redirect")


            case "handshake":
                # réponse au handshake
                #print("packet handshake reçu : handshake = ",body)

                message = "handshake="+body
                thread_anserw_handshake = Thread(target=send_packet, args=(conn,message))
                thread_anserw_handshake.start()


            case "pwd":
                pwd_infos = body.split(";")
                print(pwd_infos)

            case "404_lobby_not_exist":
                    print("This lobby does not exist.")

            case "players_pseudos":
                print(body)
                
            case "players_count":
                print(body, "joueurs / 5")
            
            case "new_player_joined":

                print(body, "a rejoint le lobby !")
                thread_players_count = Thread(target=send_packet, args=[conn, "players_count="])
                thread_players_count.start()
                
            case "refused-connection":
                print("Serveur indique : ",body)

            case "start_timer":
                ''' ICI ON RECOIT LE PAQUET START_TIMER'''
                Global_objects.game_state.depart_timer = int(body)
                Global_objects.game_state.timer = [int(body), time.time(), True]

            case "stop_timer":

                '''ICI ON RECOIT LE PAQUET D'ARRET DU TIMER (nb de joueurs inssuffisant pour continuer)'''
                Global_objects.game_state.timer[2] = False
                Global_objects.game_state.timer[0] = 20

            case 'sit_to_play_time_to_play':
                '''ICI ON RECOIT L'INDEX DU SIEGE DEVANT JOUER ET SON TEMPS RESTANT (format [0] = siège qui doit jouer / [1] = temps pour jouer)'''
                body = eval(body)
                Global_objects.parole = int(body[0]) + 1
                Global_objects.game_state.depart_timer = int(body[1])
                Global_objects.game_state.timer = [int(body[1]), time.time(), False]

            case 'pots':
                '''ICI ON RECOIT LA LISTE DES POTS ACTUELS chaque pot est sous forme d'un tuple contenant le montant du pot associé à la liste des index de sièges jouat le pot.'''
                body = eval(body)
                Global_objects.pot = int(body[0])

            case "bet":
                Global_objects.bet = int(body)

            case 'bets':
                '''RECEPTION DES MISES COURANTES liste correspondant à chaque siège où chaque None est un siège vide ou qui ne joue pas et les valeurs numériques correspondent à la valeur misée par le joueur pas encore dans le pot'''
                body = eval(body)
                Global_objects.game_bets = body

            case 'chips':
                '''RECEPTION DES CHIPS POUR CHAQUE JOUEUR, une liste correspondant aux sieges de la game, None = siege vide ou deconnecté, Valeur = chips possedés par un joueur au moment de l'envoi'''
                body = eval(body)
                for i in range(len(Global_objects.auto_arrived_sits)):
                    Global_objects.auto_arrived_sits[i][3] = body[i]

            case 'game_start':
                '''Annonce le début de la game'''
                Global_objects.game_started = True

            case 'round_start':
                '''Debut de round'''

            case 'your_turn':
                '''indique au client que c'est à lui de jouer toujours precédé de bet bets pots chips pour que le client sache sur quoi se baser. '''
                Global_objects.my_turn = True

            case "your_cards":
                print(f"###############{body}")
                '''ICI ON RECOIT LE PAQUET AVEC LES CARTES DE NOTRE MAIN SELON LA SYNTAXE INDIQUEE SUR DISCORD (ex : ["kh","1d"])
                => Pour une liste de 2 chaines de caractères, le 1er caractère c'est le rang parmi : "123456789tjqk" où t est un 10, j un valet, q une dame, k un roi et 1 un as
                => Le 2éme caractère c'est la famille parmi : hdsc =  h pour hearth, d pour diamond, s pour spade et c pour club
                Pas encore testé si tout marche'''
                body = eval(body)
                print(f"###############{body}")
                print(body)
                Global_objects.nombre_cartes = len(body)
                try:
                    print(f"###############{body}")
                    Global_objects.card_1 = body[0]
                    Global_objects.card_2 = body[1]
                except:
                    pass

            case "lobby_exists":
                # NE SACTIVE QUE SI ON DEMANDE UN LOBBY ET QU'IL EXISTE (body est l'id du lobby)
                # SI LE LOBBY N'EXISTE PAS ON GERE CA DANS 404_LOBBY_NOT_EXIST
                print(body)

            
    except Exception as e:
        print("Erreur sur network.manage_data : ",e)


def check_lobby_exist(conn,lobby_id):
    thread_ask_for_lobby = Thread(target=send_packet, args=[conn,"is_lobby_exist="+str(lobby_id)])
    thread_ask_for_lobby.start()
    # si le lobby n'existe pas tu recevras dans


def send_action(conn : socket, action : tuple):

    if action[0] == 'fold':
        packet = "my_play=fold"

    else:
        packet=f"my_play={action[0]},{str(action[1])}"
        
    thread_send_action = Thread(target=send_packet, args=[conn,packet])
    thread_send_action.start()
    


def edit_displayed_lobbys_list(liste):
    display_list = []
    for i in range(len(liste)):
        display_list.append([])
        display_list[i].append(str(liste[i][1]))
        display_list[i].append(str(liste[i][2]))
        display_list[i].append(str(liste[i][3]))
        display_list[i].append("15K")
        display_list[i].append("25K")

        display_list[i].append(str(liste[i][0]))

    Global_objects.displayed_lobbys_list = display_list
    Global_objects.serverscrollbox.servers =  Global_objects.displayed_lobbys_list


def recieve_sits_infos(liste : list,func_id : int = 0): # On gère la récéption des infos de sièges
    try :

        if func_id == 0:
            # Une liste contenant toutes les infos du joueur assi sur ce siège [sit_id, idplayer, pseudo, chips, link]
            Global_objects.auto_arrived_sits = liste

        else:
            Global_objects.func_id_dict[func_id] = liste

    except Exception as e:
        print("Erreur dans network.recieve_sits_infos : ",e)


if False:
    def send_message(client_socket : socket):
        connecte = True
        print("envoi, sur", client_socket)
        while connecte:
            if stop_sending_event.is_set():
                print("fin d'envoi sur ",client_socket)
                break

            entete = input("Entrez une entete (/disconnect pour quitter) : \n> ")
            message = input("Entrez un message (/disconnect pour quitter) : \n> ")

            if message == "/disconnect":
                break

            message = entete+"="+message
            print("message envoyé")
            
            if message == "get_lobbys=/disconnect":
                break

            else:
                try:
                    client_socket.send(message.encode("utf-8"))
                except Exception as e:
                    print("echec d'envoi de message : ",e)
                    connecte = False
                    break
                    
        
    


def start_listenning(conn : socket):
    global listenning_thread

    receive_thread = Thread(target=recieve_data, args=[conn])
    listenning_thread = receive_thread

    receive_thread.start()
if False:
    def start_sending(conn : socket):
        global sending_thread

        send_thread = Thread(target=send_message, args=[conn])
        sending_thread = send_thread

        send_thread.start()

def stop_listenning(thread : Thread):
    global stop_listenning_event
    stop_listenning_event.set()
    thread.join()

    stop_listenning_event = Event()



def stop_sending(thread : Thread):
    global stop_sending_event
    stop_sending_event.set()
    thread.join()

    stop_sending_event = Event()

def start_client():
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((host, port))

        Global_objects.client_socket = client_socket

        print("Connecté au serveur.")

        start_listenning(client_socket)

    except:
        print("Echec de connexion au serveur. (skill issue)")