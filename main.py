#Menu du jeu Poker

import pygame

#Set up de l'interface de base
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True














#fonction importante pour plus tard à laisser en bas 
def str_to_list(string: str):   #fonctionne seulement sur une liste supposée valide
    liste = []
    string = string.removeprefix("[")
    string = string.removesuffix("]")

    return string.split(",")