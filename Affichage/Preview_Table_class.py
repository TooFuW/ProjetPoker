# Preview_Table class


import pygame
from Screen_adaptation import *
import Button_class


class Preview_Table:
    """Classe Preview_Table pour afficher des previews de tables
    """

    def __init__(self, largeur_actuelle : int, hauteur_actuelle : int, screen : pygame.Surface, poker_table : pygame.Surface, pos : tuple, scale : float = 1):
        """Initialisation des paramètres des previews

        Args:
            largeur_actuelle (int): Largeur de l'écran (pour width_scale())
            hauteur_actuelle (int): Hauteur de l'écran (pour height_scale())
            screen (pygame.Surface): Ecran sur lequel afficher la fenêtre (écran de l'utilisateur)
            poker_table (pygame.Surface): Table de poker pour fond du widget
            pos (tuple): Position x, y de la preview
            scale (float) = 1: Multiplicateur de taille de la preview (1 par défaut)
        """
        self.largeur_actuelle = largeur_actuelle
        self.hauteur_actuelle = hauteur_actuelle
        self.screen = screen
        self.poker_table = poker_table
        self.x = width_scale(pos[0], largeur_actuelle)
        self.y = height_scale(pos[1], hauteur_actuelle)
        self.width = width_scale(500*scale, largeur_actuelle)
        self.height = height_scale(500*scale, hauteur_actuelle)
        self.scale = scale
        # Création de l'objet jointablebutton
        self.jointablebutton = Button_class.Button(self.largeur_actuelle, self.hauteur_actuelle, self.screen, "join table", "JOIN", "Roboto", 50, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 500*scale - 350, 500*scale - 430, (pos[0] + 180, pos[1] + 420), 6, 10)

    def draw(self):
        """Génération/affichage de la preview
        """
        # Dessinez la zone de la preview sur l'écran
        pygame.draw.rect(self.screen, "#006400", (self.x, self.y, self.width, self.height), border_radius = 10)
        # Dessine l'image de fond sur la self.screen de l'écran
        poker_table = pygame.transform.scale(self.poker_table, (width_scale(480*self.scale, self.largeur_actuelle), height_scale(390*self.scale, self.hauteur_actuelle)))
        self.screen.blit(poker_table, (self.x + 10, self.y + 10))
        # Affichage des bouttons
        # Cliquer sur le bouton JOIN fait rejoindre la table sélectionnée
        self.jointablebutton.draw()