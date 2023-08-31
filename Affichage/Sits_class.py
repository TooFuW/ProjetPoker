# Sits_class


import pygame
from Screen_adaptation import *
from Button_class import *


class Sits:

    def __init__(self, largeur_actuelle : int, hauteur_actuelle : int, screen : pygame.Surface, width : int, height : int, pos : tuple):
        self.largeur_actuelle = largeur_actuelle
        self.hauteur_actuelle = hauteur_actuelle
        self.screen = screen
        self.pos_x = width_scale(pos[0], largeur_actuelle)
        self.pos_y = height_scale(pos[1], hauteur_actuelle)
        self.pos = (self.pos_x, self.pos_y)
        self.width = width_scale(width, self.largeur_actuelle)
        self.height = height_scale(height, self.hauteur_actuelle)

    def draw(self):
        # Affichage du fond du widget de siège avec une zone noire transparente
        transparent_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 128), (0, 0, self.width, self.height), border_radius = 5)
        self.screen.blit(transparent_surface, self.pos)