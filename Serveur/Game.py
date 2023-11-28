
from Player import Player
from Sit import Sit
from typing import List
from random import randint
from Round import Round
from socket import *
from threading import *

class Game:
    """
        Represent a game wich ends when only one player got chips.

        Important : les soldes des joueurs sont stockés dans l'attribut chips de player
        pour toutes les opérations utilisant les chips in game (call,raise ...) ou hors (buy-in , claim) on utilisera cet attribut.

        start démmarre le jeu en lançant des rounds jusqu'à ce qu'un joueur gagne ou que le serveur pour x raison ferme la game. 

    """
    def __init__(self,sits : List[Sit],cave : int, players : List[Player]) -> None: # A chaque modification de sits dans le lobby, doit être modifié

        self.started = False # regarde si la game a commencé, passe à True avec self.start()
        
        self.sits = sits
        self.players = players


        self.round_nb = 0  # le nombre de round effectués dans la game
        self.dealer_index = self.first_dealer_index() #index du dealer vis à vis de la liste self.sits
        self.dealer = None  # identité du dealer

        
        
        self.cave = cave

        self.round = None
        print("game initiée.", cave)


    def start(self):
        #paie la cave pour tous les joueurs, lance les rounds jusqu'à ce qu'un joueur reste en vie.
        try:
            self.buy_in_all_players(self.cave)

            while self.check_if_we_make_new_round():
                print("round started")
                self.init_round()
                self.round.start()

        except:
            print("protocole crash")

    
    def check_if_we_make_new_round(self):
        return True # on vérifira s'il y a plus d'un joueur en vie


    def on_deconnect(self,player : Player):
        pass

    def end_game(self):
        pass

    def start_round(self):
        # Condition de démarrage du round, et démarrage
        pass

    def init_round(self):
        self.round = Round(self.sits,self.sits[self.new_dealer_index()])

    def stop_round(self):
        # Arrête le round en cours.
        pass
    

    def print_sits(self):
        for sit in self.sits:
            print(sit)

    
    def buy_in_all_players(self,sits : List[Sit] , cave : int) -> None:

        players =  [sit.get_player() for sit in sits if sit.occupied]      # Récupère tous les players assis sur un siège
        
        if len(players) == 0 or cave <= 0:
            raise ValueError
        
        for player in players:
            if type(player) == Player:
                self.buy_in(player,cave)


    def buy_in(self,player : Player, cave : int):

        """pour un joueur, va supprimer le montant de la cave de sa banque et ajouter ce montant à player.chips

        Args:
            player (Player): le joueur à qui on souhaite faire payer la cave
            cave (int): le montant de la cave

        Raises:
            TypeError: erreur de type relatif à un joueur ou à la cave
            ValueError: banque du joueur insuffisante ou cave nulle ou négative
        """
        if type(player) != Player or type(cave) != int:
            raise TypeError
        
        if player.bank < cave or cave <= 0:
            return False
        
        try:
            player.bank_remove(cave)
            player.chips += cave
            return True

        except ValueError as e:
            print("Erreur dans Game.buy_in : ",e)

    def new_dealer_index(self) -> Player:

        """passe au dealer suivant. incrémente à son appel le dealer index va s'incrémenter de 1 et prendre sa valeur modulo len(self.players) ce qui a
        pour effet de passer au suivant peu importe la taille de la liste

        Returns:
            _type_: int
        """
        
        for _ in range(len(self.sits)):

            self.dealer_index += 1
            pl = self.sits[self.dealer_index].get_player()
            if isinstance(pl,Player):  # On parcours les sièges jusqu'a ce qu'on ait un Player et il devient self.dealer
                self.dealer = pl
                return self.dealer_index
            
        self.dealer = self.sits[self.dealer_index].get_player()
        return self.dealer
        
    def first_dealer_index(self) -> int:
        self.dealer_index = randint(0,len(self.sits)-1) #le premier dealer est aléatoire

    def players_for_next_round(self):

        """On adapte les sièges pour ne garder que les joueurs pouvant jouer = joueur avec un statut connecté, joueurs avec assez de jetons pour une grosse blind 
        """



    def kick_disconnected_players(self):

        """On retire de leurs sièges tous les joueurs deconectés
        """
        changes = 0
        for sit in self.sits:
            pl = sit.get_player()
            if not pl is None:
                if not pl.connected:
                    sit.remove_player()
                    changes += 1
                    
        if changes > 0:        
            self.sits_infos_edited()

    def sits_infos_edited(self):
        print("on envoie les chanhgements à tlm")
        for pl in self.players:
            conn = pl.get_conn()
            thread_send_sits_infos = Thread(target=self.send_sits_infos, args=[conn])
            thread_send_sits_infos.start()

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



    def send_game_start(self):
        for pl in self.players:
            try:
                thread_game_start = Thread(target=self.send_packet, args=("game_start=",pl.get_conn()))
                thread_game_start.start()


            except:
                pass


    def send_packet(self, packet : str, conn : socket):
        try:
            conn.send(packet.encode("utf8"))
        except Exception as el:
            print(el)





    def is_game_winner(self):
        """renvoie True si quelqun a gagné la game (dernier joueur avec des jetons) et l'id du joueur. False sinon
        """
        pass

    def force_stop(self):
        """intervient en cas d'arret forcé de la game par le lobby, va immédiatement ajouter les chips à la banque du joueur et déconnecter tout le monde
        """
        pass



def only_players(players : list):
    for pl in players:
        if not type(pl) == Player:
            return False
    return True 

def sell_out(player : Player):
    if type(player) == Player:
        player.bank_add(player.chips)
        player.chips = 0
    else :
        raise TypeError
    
def is_one_player_alive(players : list):
    pass
    
