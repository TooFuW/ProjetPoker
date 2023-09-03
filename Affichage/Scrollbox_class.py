# Scrollbox class


import pygame
from Screen_adaptation import *
import Check_click
import Button_class


class ScrollBox:
    """Classe ScrollBox pour créer des ScrollSox (classe compliquée, pas bien écrite mais fonctionne donc éviter de modifier xD)
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
        self.indentation = "          "# Len = 10
        self.hauteurbox = 50
        self.selected = False
        # Référencement du serveur sélectionné
        self.server_selected = None

    def draw(self):
        """Génération/affichage de la scrollbox
        """
        # Créez une surface transparente
        transparent_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Dessinez le rectangle transparent sur la surface
        pygame.draw.rect(transparent_surface, (0, 0, 0, 128), (0, 0, self.width, self.height))
        
        # Afficher la surface transparente sur l'écran
        self.screen.blit(transparent_surface, (self.x, self.y))

        # Calcul de la zone d'affichage des éléments
        self.display_area = pygame.Rect(self.x, self.y, self.width, self.height)

        # Décalage initial
        item_offset_y = 0

        # Dessin des éléments visibles
        for _, server in enumerate(self.servers[self.scroll_pos:]):
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
                    if self.selected == True:
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