from socket import *
from threading import *
from strtotuple import *
from random import *


# ceci est le script qui représente les intéractions avec le serveur, il sera transposé avec la partie graphique
host, port = ('localhost', 5566)

lobbys = []

def envoi_message(client_socket : socket, msg : str):
    client_socket.send(msg.encode("utf8"))


#reception continue de messages
def receive_messages(client_socket : socket):
    connecte = True
    print("ecoute")
    while connecte:
        try:
            data = client_socket.recv(1024)
            #

            message = data.decode("utf-8")

            entete = strtotuple(message)[0]
            message = strtotuple(message)[1]

            if entete == "deconnect":
                break

            elif entete == "newplayerconnect":
                print("\n\n <<  "+message+"  >> \n\n")
            
            elif entete == "startgame":
                print("demarrage game") #a completer

            elif entete=="lobbys":
                print(message)
                try:
                    global lobbys
                    lobbys = str_to_list(message)
                except:
                    lobbys = []
                    
            else:
                print("\n[Server]: ", message)
            # Ici, vous pouvez ajouter le code pour traiter le message côté client
        except:
            print('Echec de réception.')
            break

    try :
        print("Fin d'ecoute du serveur ...")
        connecte = False
    except:
        connecte = False


#envoi continu de messages
def send_message(client_socket):
    connecte = True
    while connecte:
        entete = input("Entrez une entete (/disconnect pour quitter) : \n> ")
        message = input("Entrez un message (/disconnect pour quitter) : \n> ")

        if message == "get_lobbys=/disconnect":
            break

        message = entete+message
        print("message envoyé")
        if message == "get_lobbys=/disconnect":
            break
        else:
            client_socket.send(message.encode("utf-8"))
        
    try:
        connecte = False
        print('Deconnexion ...')
        client_socket.close()
    except:
        connecte = False


def start_client():
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((host, port))
        print("Connecté au serveur.")

        receive_thread = Thread(target=receive_messages, args=(client_socket,))
        send_thread = Thread(target=send_message, args=(client_socket,))

        envoi_pseudo = Thread(target=envoi_message, args=(client_socket, packet_pseudo))

        envoi_pseudo.start()

        receive_thread.start()
        send_thread.start()

    except:
        print("Echec de connexion au serveur. (skill issue)")

def main():
    if input("Se connecter au serveur ? (o/n)\n> ") in "oO":
        start_client()

if __name__ == "__main__":
    packet_pseudo = "pseudo="+input("Quel est votre pseudo : \n> ")
    main()


def str_to_list(string: str):   #fonctionne seulement sur une liste supposée valide
    string = string.removeprefix("[")
    string = string.removesuffix("]")

    return string.split(",")