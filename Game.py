
from Player import Player
class Game:
    """
        Represent a game wich ends when only one player got chips.

        Important : les soldes des joueurs sont stockés dans le dictionnaire : players_chips qui a pour clé l'id du joueur et pour valeur son solde
        pour toutes les opérations utilisant les chips in game (call,raise ...) ou hors (buy-in , claim) on utilisera ce dictionnaire.

        start démmarre le jeu en lançant des rounds jusqu'à ce qu'un joueur gagne ou que le serveur pour x raison ferme la game. 

    """
    def __init__(self, players : list, cave : int) -> None:

        self.round_nb = 0
        self.dealer_index = 0 #index du dealer vis à vis de la liste self.players
        self.dealer_id = 0 #identité du dealer
        self.players_chips = {}
        
        if only_players(players): #on ne veut que des joueurs dans la liste
            self.players = players
        else:
            raise TypeError
        
        self.cave = cave


    def start(self):
        #paie la cave pour tous les joueurs, envoie les paquets d'attente, attends tous les packets de confirmations, lance les rounds jusqu'à ce qu'un joueur reste en vie.
        pass
    def on_deconnect(self,player : Player):
        pass

    def end_game(self):
        pass

    def start_round(self):
        pass

    
    def buy_in_all_players(self,players : list, cave : int):
        if len(players) == 0 or cave <= 0:
            raise ValueError
        
        for player in players:
            if type(player) == Player:
                self.buy_in(player,cave)


    def buy_in(self,player : Player, cave : int):

        """pour un joueur, va supprimer le montant de la cave de sa banque et ajouter ce montant au self.players_chips pour qu'il puisse jouer avec

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
            raise ValueError
        try:
            player.bank_remove(cave)
            self.players_chips[player.get_id()] += cave

        except ValueError:
            pass

    def new_dealer(self):
        """passe au dealer suivant. incrémente à son appel le dealer index va s'incrémenter de 1 et prendre sa valeur modulo len(self.players) ce qui a
        pour effet de passer au suivant peu importe la taille de la liste

        Returns:
            _type_: None
        """
        self.dealer_index += 1
        self.dealer_index = self.dealer_index % len(self.players)

        dealer_id = self.players[self.dealer_index].get_id()
        self.dealer_id = dealer_id

    def is_game_winner(self):
        """renvoie True si quelqun a gagné la game (dernier joueur avec des jetons) et l'id du joueur. False sinon
        """
        alive_players_count = 0
        alive_players = []
        for pl in self.players:
            pl_id = pl.get_id()
            if self.players_chips[pl_id] > 0:
                alive_players.append(pl_id)

        alive_players_count = len(alive_players)
        if alive_players_count == 1:
            return True, alive_players[0]
        else:
            return False

        
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
    
