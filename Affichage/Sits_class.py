# Sits_class


import pygame
from Screen_adaptation import *
from Button_class import *


class Sits:

    def __init__(self, largeur_actuelle : int, hauteur_actuelle : int, screen : pygame.Surface, width : int, height : int, pos : tuple):
        """Initialisation de la classe Sits

        Args:
            largeur_actuelle (int): Largeur de l'écran (pour width_scale())
            hauteur_actuelle (int): Hauteur de l'écran (pour height_scale())
            screen (pygame.Surface): Ecran sur lequel afficher la fenêtre (écran de l'utilisateur)
            width (int): Largeur du widget
            height (int): Hauteur du widget
            pos (tuple): Position contenant deux valeurs x et y (x : largeur, y : hauteur)
        """
        self.largeur_actuelle = largeur_actuelle
        self.hauteur_actuelle = hauteur_actuelle
        self.screen = screen
        self.x = width_scale(pos[0], self.largeur_actuelle)
        self.y = height_scale(pos[1], self.hauteur_actuelle)
        self.width = width_scale(width, self.largeur_actuelle)
        self.height = height_scale(height, self.hauteur_actuelle)
        # Une liste contenant tous les joueurs dans la table actuelle sous la forme [sit_id, idplayer, pseudo, chips, link] par joueur
        self.player = [None, None]
   
    def draw(self):
        """Génération/affichage du siège
        """
        # Affichage du fond du widget de siège avec une zone noire transparente
        transparent_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 128), (0, 0, self.width, self.height), border_radius = 50)
        self.screen.blit(transparent_surface, (self.x, self.y))
        # Affichage des infos du joueur du siège actuel par dessus la surface transparente
        if self.player[1] is None:
            text = "Sit Available"
        else:
            text = f"{self.player[1]}\n{self.player[2]}"
            text = text.replace("'", "")
        gui_font = pygame.font.SysFont("Roboto", width_scale(30, self.largeur_actuelle))
        height = 10
        for elem in text.split("\n"):
            text_surf = gui_font.render(elem, True, "#FFFFFF")
            self.screen.blit(text_surf, (self.x + width_scale(30, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
            height += 25