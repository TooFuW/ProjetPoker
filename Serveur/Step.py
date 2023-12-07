from Board import Board
from Deck import Deck
from Sit import Sit
from typing import List
from Player import Player
from socket import *
from threading import *
from Card import Card
from Pot import Pot
from random import randint
from time import sleep

class Step:
    """

        Represent a step of the game (pre-flop, flop, turn, river) and call the methods for each player

    """
    def __init__(self,type : str ,sits : List[Sit], board : Board, deck : Deck, players : List[Player],sit_to_play_index : int, pots : List[Pot]) -> None: # Les sièges doivent être edit par le lobby à chaque changement
        
        self.started = False # passe à  True au démmarage du step
        
        self.type = type # type de la step (preflop flop turn river)
        self.sits = sits # liste des sièges de la table
        self.board = board # les cartes du centre aka le board
        self.deck = deck # la pioche
        self.players = players # liste de tous les joueurs dont les spectateurs
        self.pots = pots
        # self.player_to_play = None # important d'avoir une variable de type Player pour pouvoir comparer avec le socket envoyant la requete de jeu.
        self.func_id_dict = {}
        self.waiting_for_action_packet = False

        self.sit_to_play_index = sit_to_play_index # l'index du siège ayant la parole
        self.time_to_play = 15 # time to play par défaut, c'est bien cette valeur qui est changée à chaque decrease du timer.

        self.bet = 0 # mise courante toujours initiée à 0
        
        

    def start(self):
        print("step started")
        self.complete_round_table()

    def stop(self):
        pass

    def flop_board(self):
        cards = []
        for _ in range(3):
            card = self.deck.draw()
            cards.append(card)
            self.board.add_card(card)

        self.send_flop_packets(cards)

        

        
    def card_to_str_for_packet(card : Card):
        rank = card.get_rank()
        suit = card.get_suit()

        rank_table = {"2":"2","3":"3","4":"4","5":"5","6":"6","7":"7","8":"8","9":"9","10":"t","jack":"j","queen":"q","king":"k","ace":"1"}
        suit_table = {"club":"c","heart":"h","spade":"s","diamond":"d"}

        return rank_table[rank]+suit_table[suit]

    def turn_board(self):
        card = self.deck.draw()
        self.board.add_card(card)

        self.send_turn_packets(card)

    def river_board(self):
        card = self.deck.draw()
        self.board.add_card(card)

        self.send_river_packets(card)



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




    def send_preflop_packets(self):
        cards = [self.card_to_str_for_packet(card) for card in cards]
        packet = "preflop="

        for pl in self.players:
            thread_send_packet = Thread(target=self.send_packet, args=[packet,pl.get_conn()])
            thread_send_packet.start()



    def send_flop_packets(self, cards : List[Card]):
        cards = [self.card_to_str_for_packet(card) for card in cards]
        packet = f"flop=['{cards[0]}','{cards[1]}','{cards[2]}']"

        for pl in self.players:
            thread_send_packet = Thread(target=self.send_packet, args=[packet,pl.get_conn()])
            thread_send_packet.start()



    def send_turn_packets(self, card : Card):
        card = self.card_to_str_for_packet(card)
        packet = f"turn=['{card}']"

        for pl in self.players:
            thread_send_packet = Thread(target=self.send_packet, args=[packet,pl.get_conn()])
            thread_send_packet.start()



    def send_river_packets(self, card : Card):
        card = self.card_to_str_for_packet(card)
        packet = f"river=['{card}']"

        for pl in self.players:
            thread_send_packet = Thread(target=self.send_packet, args=[packet,pl.get_conn()])
            thread_send_packet.start()
            






    def ask_player_to_play(self):
        """La demande du tour de jeu d'un joueur.

        on passe self.waiting_for_action_packet à True
        on passe le numéro 60 du self.func_id_dict à None signifiant qu'aucune action de jeu n'a été récupérée
        on envoie le paquet de demande d'action de jeu.
        on envoit sit_to_play_time_to_play à tlm
        on lance le protocole timer à 15 secondes 

        si on reçoit une action de jeu dans lobby :
            le code 60 est remplaçé par Lobby qui y mettra l'action de jeu
            le timer s'arrette
            on passe self.waiting_for_action_packet à False
            on stocke l'action de jeu dans une variable tmp
            on repasse le code 60 du dict à None
            on renvoie l'action de jeu
            fin

        si le timer s'arrette sans action de jeu reçue :
            le code 60 reste à None
            on passe self.waiting_for_action_packet à False
            on s'assure que le joueur soit warned
            on renvoie l'action de jeu suivante : Fold
            fin


        """
        
        conn = self.sits[self.sit_to_play_index].get_player().get_conn()
        
        self.waiting_for_action_packet = True # set l'attente de paquet d'action à vrai

        self.add_func_id_dict(60,None) # l'action de jeu courante est None
        thread_packet = Thread(target=self.send_packet, args=["your_turn=",conn]) # on previent le joueur qui doit jouer
        thread_packet.start()
        
        brcst_packet = f"sit_to_play_time_to_play=({str(self.sit_to_play_index)},{str(self.time_to_play)})" #on annonce à tous les autres à qui c'est de jouer
        thread_brcst_packet = Thread(target=self.broadcast_packet, args=[brcst_packet])
        thread_brcst_packet.start()
        print("packet ask to play envoyé.")

        # protocole timer

        while self.func_id_dict[60] is None and self.time_to_play > 0: #tant que le joueur n'a pas joué ou que le timer n'est pad 0
            # on attends que le joueur joue
            print(self.time_to_play)
            sleep(1)
            self.time_to_play -= 1

        self.waiting_for_action_packet = False
        tmp = self.func_id_dict[60]
        
        if tmp is None:
            pass
            print("pas reçu de réponse")
            #on fait en sorte de warn car il n'a pas répondu dans les delais
        print("réponse reçue")
        self.func_id_dict[60] = None
        return tmp




    def complete_round_table(self):
        """Decrit un tour de table complet où on va demander à chaque joueur son action de jeu et display les actions de jeux 
        en quelque sorte la mainloop du jeu

        la Step s'acheve à la fin de cette fonction et qq ajustements finaux le tout dans la fonction main.

        On send_table_infos()

        Tant que la Step n'est pas finie :
            On ask_player_to_play()
            l'action de jeu une fois obtenue on édite tout ce qu'il y a à éditer
            On passe Sit_to_play au suivant et Time_to_play à 15 (en passant au suivant on s'assure que le mecs a des chips (ce serait pratique))
            On send_table_infos()
            

        
        """
        
        self.broadcast_packet("step_start=")

        self.send_table_infos()

        while not self.is_step_done():

            self.ask_player_to_play()


            action = self.func_id_dict[60]
            if not action is None:
                self.manage_player_action(action)
            else:
                self.manage_player_action("fold") # attention ce joueur n'a pas joué dans les delais il doit etre averti


            pl = self.sits[self.sit_to_play_index].get_player()

            if not pl is None:
            
                if pl.state == "peut_parler":
                    pl.state = "a_parle"

            self.set_next_sit_to_play()
            self.time_to_play = 15
            self.send_table_infos()



    def manage_player_action(self, action : str):
        """_summary_

        Args:
            player (Player): Le joueur effectuant l'action
            action (str): l'action, un str contenant 2 mots séparés par une virgule

        Une action de type fold couchera le joueur
        Une action de type bet fait miser le joueur avec ses chips
        si l'action Bet a un montant de 0 c'est un check, on vérifie alors si c'est possible
        si l'action Bet est un montant superieur ou égal aux chips du joueur c'est un All-In on fait tt le protocole
        
        un paquet au format invalide ou demandant une action invalide couchera le joueur.
        """

        # on commence par transformer le paquet en tuple si c'est possible
        # NE SURTOUT PAS UTILISER EVAL COTE SERVEUR c'est dangereux et ouvre la porte à des failles d'injection python

        player = self.sits[self.sit_to_play_index].get_player()
        action = action.split(",")

        action_type = action[0]

        if action_type == 'fold': # action valide de type fold
            '''Protocole fold'''
            print("fold du player")
            self.fold_player(player)

        else:
            if action_type == 'bet':

                if len(action) == 2:
                    amount = action[1]

                    try:
                        amount = int(amount) # action valide de type bet

                        if amount < 0 :
                            # attention un ptit malin a réussi à envoyer un paquet avec des valeurs négatives

                            self.fold_player(player)
                            print('action invalide')

                        else:

                            if amount >= player.get_chips():
                                
                                if player.get_chips() > 0:

                                    self.all_in_player(player)

                                pass #action valide de type all-in

                            else:

                                self.bet_player(amount)





                    except:
                        print("action invalide.")
                        self.fold_player()




    def fold_player(self,player : Player):
        player.state = 'fold'

    def all_in_player(self,player : Player):

        player.state = 'all-in'
        player.bet += player.chips
        player.chips = 0

        if player.bet > self.bet:
                # si la mise augmente
                self.bet = player.bet
                self.bet_been_raised()


    def bet_player(self,player : Player, amount):

        if amount >= player.chips:
            self.all_in_player(player)

        else:
            if amount > 0:
                player.bet += amount
                player.chips -= amount


            if player.bet > self.bet:
                # si la mise augmente
                self.bet = player.bet
                self.bet_been_raised()

    def bet_been_raised(self):
        # ici le protocole lorsque la mise à suivre a été augmentée = on passe tous les players a_parlé en peut_parler SAUF le player qui a produit ce changement.
        for sit in self.sits:
            pl = sit.get_player()
            if not pl is None:
                if pl.state == "a_parle":
                    pl.state = "peut_parler"


    def is_step_done(self):
        print("verif step est finie.")
        # la step est terminée quand tout les joueurs sont d'accord sur un prix donc quand toute la table est soit fold soit en all-in soit en a_parle

        for sit in self.sits:
            pl = sit.get_player()
            if not pl is None:
                if not pl.state in ("fold","all-in","a_parle"):
                    print("step n'est pas finie.")
                    return False
        print("step est finie.")
        return True
    
    def set_next_sit_to_play(self):
        print("choix du prochain joueur à parler")

        lenght = len(self.sits)

        for i in range(lenght):
            next_sit = (self.sit_to_play_index + i + 1) % lenght # permet de revenir au debut des index apres un tour complet evidemment
            pl = self.sits[next_sit].get_player()
            if not pl is None:
                print(pl.pseudo,pl.state)
                if pl.state == "peut_parler":
                    self.sit_to_play_index = next_sit
        print("nouveau siege à jouer :",self.sit_to_play_index)




    def send_bet(self,player : Player):
        conn = player.get_conn()
        packet = "bet="+str(self.bet)

        thread_send_bet = Thread(target=self.send_packet, args=[packet,conn])
        thread_send_bet.start()




            
    def send_sit_to_play(self,conn):
        packet = f"sit_to_play_time_to_play=({str(self.sit_to_play_index)},{str(self.time_to_play)})"
        thread_send = Thread(target=self.send_packet,args=[conn,packet])
        thread_send.start()





    def broadcast_sit_to_play(self):
        for pl in self.players:
            conn = pl.get_conn()
            thread_send_sit = Thread(target=self.send_sit_to_play,args=(conn))
            thread_send_sit.start()




    def broadcast_packet(self,packet):
        for pl in self.players:
            conn = pl.get_conn()
            thread_send_sit = Thread(target=self.send_packet,args=(packet,conn))
            thread_send_sit.start()




    def send_table_infos(self):
        """TRES IMPORTANT 
        cette fonction va broadcast à tous les joueurs le montant de la mise courante, les mises de chacun, les pots, les chips
        aka les infos de bases à avoir après chaque action 
        """

        # send bets
        tmp_bets = []
        for sit in self.sits:
            pl = sit.get_player()
            if pl == None:
                tmp_bets.append('None')
            else:
                tmp_bets.append(str(pl.bet))

        bets_packet = "bets="+str(tmp_bets)
        self.broadcast_packet(bets_packet)
        

        # send pots
        self.broadcast_packet("pots="+str(self.pots))

        # send bet
        self.broadcast_packet("bet="+str(self.bet))


        # send chips des joueurs
        chips = []
        for sit in self.sits:
            pl = sit.get_player()
            if not pl is None:
                chips.append(pl.get_chips())
            else:
                chips.append(None)

        self.broadcast_packet("chips="+str(chips))






    def send_packet(self, packet : str, conn : socket):
        try:
            conn.send(packet.encode("utf8"))
        except Exception as el:
            print(el)




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




    def sits_infos_edited(self):
        print("on envoie les chanhgements à tlm")
        for pl in self.players:
            conn = pl.get_conn()
            thread_send_sits_infos = Thread(target=self.send_sits_infos, args=[conn])
            thread_send_sits_infos.start()



