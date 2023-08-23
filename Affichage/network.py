from socket import *
from threading import *
from strtotuple import *
from random import *
from str_to_list import *
import Global_objects

host, port = ('localhost', 5566)

lobbys = []

global socket_lobby
socket_lobby = None

def envoi_message(client_socket : socket, msg : str):
    client_socket.send(msg.encode("utf8"))

def ask_lobbys(client_socket):
    thread_ask_lobbys = Thread(target=envoi_message, args=(client_socket, "get_lobbys="))
    thread_ask_lobbys.start()
#reception continue de messages
def recieve_data(client_socket : socket):
    connecte = True
    print("écoute, sur", client_socket)
    while connecte:
        try:
            data = client_socket.recv(1024)
            #

            message = data.decode("utf-8")

            entete = strtotuple(message)[0]
            message = strtotuple(message)[1]

            match entete:

                case "deconnect":
                    break

                case "newplayerconnect":
                    print("\n\n <<  "+message+"  >> \n\n")
                
                case "startgame":
                    print("demarrage game") #a completer

                case "lobbys":
                    try:
                        global lobbys
                        lobbys = str_to_lists_in_list(message)
                        list_lobbys_convert_str(lobbys)
                        print(lobbys, type(lobbys))
                        Global_objects.lobbys_list = lobbys
                        for i in lobbys:
                            print(i, type(i))
                        
                        edit_displayed_lobbys_list(lobbys)
                    except:
                        lobbys = []
                        Global_objects.lobbys_list = lobbys

                case "redirect":
                    try:
                        message = message.split(":")
                        host,port = message[0],int(message[1])
                        client_socket_lobby = socket(AF_INET, SOCK_STREAM)
                        Global_objects.client_socket = client_socket
                        client_socket_lobby.connect((host, port))
                        print("Connecté au lobby.", host, port)
                        listen_lobby = Thread(target=recieve_data, args=[client_socket_lobby])
                        global socket_lobby
                        socket_lobby = client_socket_lobby
                        
                        client_socket.close()

                        # a suivre ...

                    
                    except:
                        pass #packet echec

                case "404_lobby_not_exist":
                    print("This lobby does not exist.")

                case "players_pseudos":
                    print(message)
                case "players_count":
                    print(message, "joueurs / 5")
                case "new_player_joined":
                    print(message, "a rejoint le lobby !")
                    thread_players_count = Thread(target=envoi_message, args=[client_socket, "players_count="])
                    thread_players_count.start()
                    
    
            # Ici, vous pouvez ajouter le code pour traiter le message côté client
        except:
            print('Echec de réception.')
            connecte = False

    try :
        print("Fin d'ecoute du serveur ...")
        connecte = False
        try:
            print("ecoute des packets en provenance du lobby")
            listen_lobby.start()
        except:
            print("echec de connexion au lobby")
    except:
        connecte = False

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

def send_message(client_socket):
    connecte = True
    print("envoi, sur", client_socket)
    while connecte:
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
            except:
                print("echec d'envoi de message")
                break
        
    try:
        global socket_lobby
        if not socket_lobby is None :
            print(socket_lobby)
            send_message_lobby = Thread(target=send_message, args=[socket_lobby])
            socket_lobby = None
            send_message_lobby.start()

        else: 
            connecte = False
            print('Deconnexion ...')
            client_socket.close()
    except:
        connecte = False

def start_client():
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        Global_objects.client_socket = client_socket
        client_socket.connect((host, port))
        print("Connecté au serveur.")

        receive_thread = Thread(target=recieve_data, args=(client_socket,))
        send_thread = Thread(target=send_message, args=(client_socket,))


        receive_thread.start()
        send_thread.start()

    except:
        print("Echec de connexion au serveur. (skill issue)")