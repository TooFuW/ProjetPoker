
from Player import Player
class Game:
    """
        Represent a game wich ends when only one player got chips.

    """
    def __init__(self, players : list, cave : int) -> None:
        pass

    def start(self):
        #paie la cave pour tous les joueurs, envoie les paquets d'attente, attends tous les packets de confirmations, lance les rounds jusqu'à ce qu'un joueur reste en vie.
        pass
    def on_deconnect(self,player : Player):
        pass

    def end_game(self):
        pass

    def start_round(self):
        pass



def buy_in_all_players(players : list, cave : int):
    if len(players) == 0 or cave <= 0:
        raise ValueError
    
    for player in players:
        if type(player) == Player:
            player.chips = cave
            player.bank_remove(cave)

def buy_in(player : Player, cave : int):
    if type(player) != Player or type(cave) != int:
        raise TypeError
    if len(player) == 0 or cave <= 0:
        raise ValueError
    
    player.bank_remove(cave)
    player.chips += cave

def claim_chips(player : Player):
    if type(player) == Player:
        player.bank_add(player.chips)
        player.chips = 0
    else :
        raise TypeError
    
def is_one_player_alive(players : list):
    pass
    
