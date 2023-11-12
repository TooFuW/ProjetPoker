"""Document contenant la classe ScrollBox qui permet d'afficher une liste de tous les serveurs disponibles et de sélectionner celui qu'on veut"""


import pygame
from Screen_adaptation import *
import Check_click
import Button_class


class ScrollBox:
    """Classe ScrollBox pour créer des scrollbox contenant une "liste" de boutons, chacun relié à un serveur donné
    """

    def __init__(self, largeur_actuelle : int, hauteur_actuelle : int, screen : pygame.Surface, x : int, y : int, width : int, height : int, servers : list):
        """Initialisation de la classe ScrollBox

        Args:
            largeur_actuelle (int): Largeur de l'écran (pour width_scale())
            hauteur_actuelle (int): Hauteur de l'écran (pour height_scale())
            screen (pygame.Surface): Ecran sur lequel afficher la fenêtre (écran de l'utilisateur)
            x (int): Position x de la scrollbox (Largeur)
            y (int): Position y de la scrollbox (Hauteur)
            width (int): Largeur de la scrollbox
            height (int): Hauteur de la scrollbox
            servers (list): Liste des serveurs/tables à afficher
        """
        self.largeur_actuelle = largeur_actuelle
        self.hauteur_actuelle = hauteur_actuelle
        self.screen = screen
        self.x = width_scale(x, largeur_actuelle)
        self.default_x = x
        self.y = height_scale(y, hauteur_actuelle)
        self.default_y = y
        self.width = width_scale(width, largeur_actuelle)
        self.default_width = width
        self.height = height_scale(height, hauteur_actuelle)
        self.servers = servers
        # Position de la scrollbox à partir du point de départ (0)
        self.scroll_pos = 0
        self.indentation = " "*width_scale(35, self.largeur_actuelle, True)
        self.hauteurbox = 50
        self.selected = False
        # Référencement du serveur sélectionné
        self.server_selected = None
        # Calcul de la zone d'affichage des éléments
        self.display_area = pygame.Rect(self.x, self.y- height_scale(3, self.hauteur_actuelle), self.width, self.height + height_scale(15, self.hauteur_actuelle))

    def draw(self):
        """Génération/affichage de la scrollbox
        """
        # Créez une surface transparente
        transparent_surface = pygame.Surface((self.width, self.height + height_scale(15, self.hauteur_actuelle)), pygame.SRCALPHA)

        # Dessinez le rectangle transparent sur la surface
        pygame.draw.rect(transparent_surface, (0, 0, 0, 200), (0, 0, self.width, self.height + height_scale(15, self.hauteur_actuelle)))
        
        # Afficher la surface transparente sur l'écran
        self.screen.blit(transparent_surface, (self.x, self.y - height_scale(3, self.hauteur_actuelle)))

        # Décalage initial
        item_offset_y = 0

        # Dessin des éléments visibles
        for i, server in enumerate(self.servers[self.scroll_pos:]):
            if i < 13:
                item_y = self.default_y + item_offset_y
                # Délimitation de la zone de la scrollbox
                text = (server[0] + self.indentation + str(server[1]) + self.indentation + server[2] + self.indentation + server[3] + self.indentation + server[4] + self.indentation + server[5])
                item_rect = Button_class.Button(self.largeur_actuelle, self.hauteur_actuelle, self.screen, "server", text, "Roboto", 24, "#475F77", "#354B5E", "#D74B4B", "#354B5E", self.default_width, self.hauteurbox, (self.default_x, item_y), 3, 0)
                item_rect.check_click()
                mouse_pos = pygame.mouse.get_pos()
                # Quand un bouton de serveur est cliqué
                if item_rect.top_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:
                        self.selected = True
                        self.server_selected = item_rect
                    else:
                        if self.selected:
                            self.selected = False
                            Check_click.check_click(self.server_selected)
                # Affichage des serveurs disponibles
                if item_rect.top_rect.colliderect(self.display_area):
                    item_rect.draw()
                # Ajouter un padding entre chaque serveur
                item_offset_y += self.hauteurbox + 10  # Ajouter 10 pixels de padding

    def scroll_up(self):
        """Pour scroller vers le haut
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.display_area.collidepoint(mouse_pos):
            if self.scroll_pos > 0:
                self.scroll_pos -= 1

    def scroll_down(self):
        """Pour scroller vers le bas
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.display_area.collidepoint(mouse_pos):
            if self.scroll_pos < width_scale((len(self.servers) - 1) - (self.height // (self.hauteurbox + 10)), self.largeur_actuelle):
                self.scroll_pos += 1