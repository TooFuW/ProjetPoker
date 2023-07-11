
from Player import Player
class Game:
    """
        Represent a game wich ends when only one player got chips.

    """
    def __init__(self, players : list, cave : int) -> None:
        pass

    def start(self):
        pass


def buy_in_all(players : list, cave : int):
    if len(players) == 0 or cave <= 0:
        raise ValueError
    
    for player in players:
        if type(player) == Player:
            player.chips = cave
            player.bank_remove(cave)

def claim_chips(player : Player):
    if type(player) == Player:
        player.bank_add(player.chips)
        player.chips = 0
    else :
        raise TypeError
