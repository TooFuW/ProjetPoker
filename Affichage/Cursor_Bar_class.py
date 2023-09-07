# Cursor_Bar_class


import pygame
from Screen_adaptation import *
import Global_objects


class Cursor_Bar:

    def __init__(self, largeur_actuelle : int, hauteur_actuelle : int, screen : pygame.Surface, width : int, height : int, pos : tuple, bar_color : str or int, cursor_color : str or int, text_color : str or int, cursor_basic_pos : int):
        """Initialisation de la classe Cursor_bar

        Args:
            largeur_actuelle (int): Largeur de l'écran (pour width_scale())
            hauteur_actuelle (int): Hauteur de l'écran (pour height_scale())
            screen (pygame.Surface): Ecran sur lequel afficher la fenêtre (écran de l'utilisateur)
           width (int): Largeur de la barre
            height (int): Hauteur de la barre
            pos (tuple): Position contenant deux valeurs x et y (x : largeur, y : hauteur)
            bar_color (strorint): Couleur de la barre
            cursor_color (strorint): Couleur du curseur
            cursor_basic_pos (int): Position de départ du curseur en largeur
        """
        self.largeur_actuelle = largeur_actuelle
        self.hauteur_actuelle = hauteur_actuelle
        self.screen = screen
        self.width = width_scale(width, self.largeur_actuelle)
        self.height = height_scale(height, self.hauteur_actuelle)
        self.x = width_scale(pos[0], self.largeur_actuelle)
        self.y = height_scale(pos[1], self.hauteur_actuelle)
        self.bar_color = bar_color
        self.cursor_color = cursor_color
        self.text_color = text_color
        self.cursor_width = cursor_basic_pos
        self.is_selected = False

    def draw(self, variable, text_size : int):
        """On dessine la cursor_bar

        Args:
            variable (variable): Valeur à afficher
            text_size (int): Taille du texte
        """
        mouse_pos = pygame.mouse.get_pos()
        # Création du curseur et de la barre derrière
        bar = pygame.draw.rect(self.screen, self.bar_color, pygame.Rect((self.x, self.y), (self.width, self.height)), border_radius = 10)
        cursor = pygame.draw.circle(self.screen, self.cursor_color, (self.cursor_width, self.y + self.height//2), self.height)
        # On change la pos x du curseur lorsque l'on clique dessus, sans dépasser les bordures
        if cursor.collidepoint(mouse_pos) or bar.collidepoint(mouse_pos):
            # On affiche les infos du curseur si la souris est dessus
            info = pygame.draw.circle(self.screen, self.cursor_color, (cursor.centerx, cursor.centery + cursor.height), max(cursor.width//4, width_scale(10, self.largeur_actuelle)))
            info_surf = pygame.Rect((info.centerx - info.width//2, info.centery), (info.width, info.height))
            pygame.draw.rect(self.screen, self.cursor_color, info_surf, border_radius = 1)
            text = f"{variable}"
            font = pygame.font.SysFont("Roboto", width_scale(text_size, self.largeur_actuelle))
            text_info = font.render(text, True, self.text_color)
            text_rect = text_info.get_rect(center = info_surf.center)
            self.screen.blit(text_info, text_rect)
            if pygame.mouse.get_pressed()[0]:
                self.is_selected = True
                Global_objects.buttons_interactibles = False
        # Amélioration de l'interaction avec le curseur
        if self.is_selected is True:
            if not pygame.mouse.get_pressed()[0]:
                self.is_selected = False
                Global_objects.buttons_interactibles = True
            else:
                self.cursor_width = mouse_pos[0]
                # On affiche les infos du curseur si la souris est dessus
                info = pygame.draw.circle(self.screen, self.cursor_color, (cursor.centerx, cursor.centery + cursor.height), max(cursor.width//4, width_scale(10, self.largeur_actuelle)))
                info_surf = pygame.Rect((info.centerx - info.width//2, info.centery), (info.width, info.height))
                pygame.draw.rect(self.screen, self.cursor_color, info_surf, border_radius = 1)
                text = f"{variable}"
                font = pygame.font.SysFont("Roboto", width_scale(text_size, self.largeur_actuelle))
                text_info = font.render(text, True, self.text_color)
                text_rect = text_info.get_rect(center = info_surf.center)
                self.screen.blit(text_info, text_rect)
                # On gére les cas où l'utilisateur pousserait le curseur en dehors de la barre
                if self.cursor_width >= self.x + self.width:
                    self.cursor_width = self.x + self.width
                elif self.cursor_width <= self.x:
                    self.cursor_width = self.x
        # On vérifie en dehors du if les cas où l'utilisateur pousserait le curseur en dehors de la barre
        if self.cursor_width >= self.x + self.width:
            self.cursor_width = self.x + self.width
        elif self.cursor_width <= self.x:
            self.cursor_width = self.x