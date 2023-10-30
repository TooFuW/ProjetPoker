"""Document contenant la classe TextInputBox qui permet de créer des boxs où l'utilisateur peut entrer du texte tout en ayant une myriade de paramètres"""


import pygame
from Screen_adaptation import *
from icecream import ic


class TextInputBox:
    """Classe TextInputBox pour gérer des input de texte (https://www.youtube.com/watch?v=Rvcyf4HsWiw&t=323s)
    """

    def __init__(self, largeur_actuelle : int, hauteur_actuelle : int, screen : pygame.Surface, text_size : int, pos : tuple, width : int, height : int, active_color : str, passive_color : str, base_size : int, adaptative : bool = True, max_caracteres : int = -1, num_only : bool = False, interactible : bool = True, starting_text : str = ""):
        """Initialisation des paramètres des TextInputBox

        Args:
            largeur_actuelle (int): Largeur de l'écran (pour width_scale())
            hauteur_actuelle (int): Hauteur de l'écran (pour height_scale())
            screen (pygame.Surface): Ecran sur lequel afficher la fenêtre (écran de l'utilisateur)
            text_size (int): Taille du texte
            pos (tuple): Position x, y de la boîte (x : largeur, y : hauteur)
            width (int): Largeur de la boîte
            height (int): Hauteur de la boîte
            active_color (str): Couleur de la boîte lorsque l'on peut écrire dedans
            passive_color (str): Couleur de la boîte lorsque l'on ne peut pas écrire dedans
            base_size (int): Taille minimum de la box (DOIT ETRE EGAL A WIDTH SI ADAPTATIVE = FALSE)
            adaptative (bool) = True: True si la taille de la boîte peut changer en fonction de la taille du texte, False si elle est fixe (le texte ne pourra alors pas dépasser de la boîte)
            max_caracteres (int) = -1: -1 si les caractères sont illimités, entier positif sinon
            num_only (bool) = False: True si on ne peut entrer que des chiffres, False sinon
            interactible (bool) = True: True si on peut interagir avec, False sinon
            starting_text (str) = "": Chaîne de caractère vide par défaut, sinon le texte de départ
        """
        self.largeur_actuelle = largeur_actuelle
        self.hauteur_actuelle = hauteur_actuelle
        self.screen = screen
        # Paramères du texte
        self.base_font = pygame.font.SysFont("Roboto", width_scale(text_size, largeur_actuelle))
        # Texte "pur"
        self.user_text = starting_text
        self.max_caracteres = max_caracteres
        # Position du texte
        self.input_rect = pygame.Rect(width_scale(pos[0], largeur_actuelle), height_scale(pos[1], hauteur_actuelle), width_scale(width, largeur_actuelle), height_scale(height, hauteur_actuelle))
        # Couleur de la box en fonction si elle est sélecionnée ou non
        self.color_active = active_color
        self.color_passive = passive_color
        self.color = self.color_passive
        # Vérifie si on peut input du texte
        self.active = False
        self.base_size = width_scale(base_size, self.largeur_actuelle)
        self.adaptative_size = adaptative
        self.text_size = 0
        self.num_only = num_only
        self.interactible = interactible
        # Texte à dessiner
        self.draw_text = ""
        self.backspace = False
    
    def draw(self):
        """On dessine la box et le texte écrit par l'utilisateur
        """
        # On récupére la position de la souris
        mouse_pos = pygame.mouse.get_pos()
        # On vérifie si la box a été sélectionnée
        if pygame.mouse.get_pressed()[0]:
            if self.interactible:
                if self.input_rect.collidepoint(mouse_pos):
                    self.active = True
                else:
                    self.active = False
        # On définit la couleur de la box en fonction de si elle est sélectionnée ou non
        if self.active:
                self.color = self.color_active
        else:
            self.color = self.color_passive
        # On dessine le texte et la box
        pygame.draw.rect(self.screen, self.color, self.input_rect, border_radius = 10)
        # On fait des sauts à la ligne si nécessaire
        self.draw_text = ""
        for caract in self.user_text:
            text_actuel = self.draw_text.split("\n")
            text_surface = self.base_font.render(text_actuel[-1], True, "#FFFFFF")
            if text_surface.get_width() >= self.base_size - width_scale(25, self.largeur_actuelle) and not self.adaptative_size:
                self.draw_text += f"\n{caract}"
            else:
                self.draw_text += caract
        # Dessin du texte par lignes si la box n'est pas adaptative et que le texte dépasse, sinon le texte est dessiné normalement
        if not self.adaptative_size:
            y = self.input_rect.y + 5
            for line in self.draw_text.split("\n"):
                text_surface = self.base_font.render(line, True, "#FFFFFF")
                self.screen.blit(text_surface, (self.input_rect.x + 5, y))
                y += text_surface.get_height()
        else:
            text_surface = self.base_font.render(self.draw_text, True, "#FFFFFF")
            self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        # On crée une taille de box adaptative
        if self.adaptative_size:
            # Taille de la box qui est de base 200 et qui augmente si le texte dépasse
            self.input_rect.w = max(self.base_size, text_surface.get_width() + width_scale(10, self.largeur_actuelle))
        else:
            # Si le texte dépasse mais que la box n'est pas adaptative on retourne à la ligne
            try:
                if self.draw_text[-1] == "\n":
                    self.draw_text = self.draw_text[:-1]
            except:
                pass