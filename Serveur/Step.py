from Board import Board
from Deck import Deck
from Sit import Sit
from typing import List
from Player import Player
from socket import *
from threading import *
from Card import Card

class Step:
    """

        Represent a step of the game (pre-flop, flop, turn, river) and call the methods for each player

    """
    def __init__(self,type : str ,sits : List[Sit], board : Board, deck : Deck, players : List[Player]) -> None: # Les sièges doivent être edit par le lobby à chaque changement
        
        self.started = False # passe à  True au démmarage du step
        
        self.type = type
        self.sits = sits
        self.board = board
        self.deck = deck
        self.players = players

        self.bet = 0
        

    def start(self):
        pass

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

    def turn_board(self):
        card = self.deck.draw()
        self.board.add_card(card)

        self.send_turn_packets(card)

    def river_board(self):
        card = self.deck.draw()
        self.board.add_card(card)

        self.send_river_packets(card)


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
            

    def ask_player_to_play(self, player : Player):
        conn = player.get_conn()
        thread_packet = Thread(target=self.send_packet, args=["your_turn=",conn])

    def send_bet(self,player : Player):
        conn = player.get_conn()
        packet = "bet="+str(self.bet)

        thread_send_bet = Thread(target=self.send_packet, args=[packet,conn])
        thread_send_bet.start()
            





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



