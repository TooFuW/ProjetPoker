# Sits_class


import pygame
from Screen_adaptation import *
from Button_class import *


class Sits:

    def __init__(self, largeur_actuelle : int, hauteur_actuelle : int, screen : pygame.Surface):
        self.largeur_actuelle = largeur_actuelle
        self.hauteur_actuelle = hauteur_actuelle
        self.screen = screen

    def draw(self):
        pass