from socket import *
from threading import *
from packet_separator import *
from random import *
import Global_objects
import time
from datetime import datetime

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
            time.sleep(0.1)

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
                    print("redirection...")

                    body = body.split(":")
                    host,port = body[0],int(body[1])
                    # fermeture de l'ancien socket
                    Global_objects.client_socket.close()
                    # création du socket lobby
                    client_socket_lobby = socket(AF_INET, SOCK_STREAM)
                    

                    # attribution du nouveau socket à la variable globale
                    Global_objects.client_socket = client_socket_lobby

                    client_socket_lobby.connect((host, port))
                    print("Connecté au lobby.", host, port)

                    global sending_thread
                    global listenning_thread

                    stop_sending(sending_thread)
                    stop_listenning(sending_thread)

                    start_sending(Global_objects.client_socket)
                    start_listenning(Global_objects.client_socket)
                        # a suivre ...

                    
                except:
                    print("Erreur network.manage_data case redirect")


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


    except Exception as e:
        print("Erreur sur network.manage_data : ",e)


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
    print("IMPORTANT :")
    print(Global_objects.displayed_lobbys_list)


def recieve_sits_infos(liste : list,func_id : int = 0): # On gère la récéption des infos de sièges
    try :

        if func_id == 0:
            Global_objects.auto_arrived_sits = liste

        else:
            Global_objects.func_id_dict[func_id] = liste

        if False:
            # On affecte les infos de sièges à la bonne variable
            print("\n\nokkkk\n\n")
            if Global_objects.is_selecting_sit[0] is True:
                # Si l'utilisateur sélectionne un siège, on cherche quel siège il a sélectionné afin d'y attribuer les nouvelles valeurs du siège
                match Global_objects.is_selecting_sit[1]:
                    case 0:
                        Global_objects.sit_1.player = liste
                    case 1:
                        Global_objects.sit_2.player = liste
                    case 2:
                        Global_objects.sit_3.player = liste
                    case 3:
                        Global_objects.sit_4.player = liste
                    case 4:
                        Global_objects.sit_5.player = liste
                    case 5:
                        Global_objects.sit_6.player = liste
                    case 6:
                        Global_objects.sit_7.player = liste
                    case 7:
                        Global_objects.sit_8.player = liste
                    case 8:
                        Global_objects.sit_9.player = liste
                    case 9:
                        Global_objects.sit_10.player = liste
                Global_objects.is_selecting_sit = [False, -1]
            else:
                Global_objects.previewlobbys.players = liste
    except Exception as e:
        print("Erreur dans network.recieve_sits_infos : ",e)



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
        start_sending(client_socket)

    except:
        print("Echec de connexion au serveur. (skill issue)")