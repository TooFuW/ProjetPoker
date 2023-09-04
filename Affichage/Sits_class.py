# Sits_class


import pygame
from Screen_adaptation import *
from Button_class import *
import Global_objects
from Check_click import *


class Sits:

    def __init__(self, largeur_actuelle : int, hauteur_actuelle : int, screen : pygame.Surface, width : int, height : int, pos : tuple, profile_picture : str):
        """Initialisation de la classe Sits

        Args:
            largeur_actuelle (int): Largeur de l'écran (pour width_scale())
            hauteur_actuelle (int): Hauteur de l'écran (pour height_scale())
            screen (pygame.Surface): Ecran sur lequel afficher la fenêtre (écran de l'utilisateur)
            width (int): Largeur du widget
            height (int): Hauteur du widget
            pos (tuple): Position contenant deux valeurs x et y (x : largeur, y : hauteur)
            profile_picture (str): Lien de la pdp du joueur
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
        self.profile_picture = pygame.transform.scale(profile_picture, (width_scale(120, largeur_actuelle), height_scale(120, hauteur_actuelle)))
        self.selected = False
        # Référencement du siège sélectionné
        self.sit_selected = None
   
    def draw(self):
        """Génération/affichage du siège
        """
        # Affichage du fond du widget de siège
        # On affiche le bouton pour s'asseoir si le joueur n'est pas encore assis
        if Global_objects.is_selecting_sit[0] is True and self.player[1] is None:
            sitbutton = Button(self.largeur_actuelle, self.hauteur_actuelle, self.screen, f"sit {self.player[0] + 1}", f"Sit down [{self.player[0] + 1}]", "Roboto", 30, "#475F77", "#354B5E", "#D74B4B", "#354B5E", self.width, self.height, (self.x, self.y), 6, 50)
            sitbutton.check_click()
            sitbutton.draw()
            mouse_pos = pygame.mouse.get_pos()
            # Quand le bouton de siège est cliqué
            if sitbutton.top_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    self.selected = True
                    self.sit_selected = sitbutton
                else:
                    if self.selected == True:
                        self.selected = False
                        check_click(self.sit_selected)
        # Sinon on affiche directement les infos du siège
        else:
            transparent_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(transparent_surface, (0, 0, 0, 128), (0, 0, self.width, self.height), border_radius = 50)
            self.screen.blit(transparent_surface, (self.x, self.y))
            # On affiche la pdp du joueur
            self.screen.blit(self.profile_picture, (self.x - width_scale(65, self.largeur_actuelle), self.y - height_scale(22, self.hauteur_actuelle)))
        # Affichage des infos du joueur du siège actuel par dessus la surface transparente
        if self.player[1] is None:
            text = "Sit Available"
        else:
            text = f"{self.player[1]}\n{self.player[2]}"
            text = text.replace("'", "")
        gui_font = pygame.font.SysFont("Roboto", width_scale(30, self.largeur_actuelle))
        height = 10
        if Global_objects.is_selecting_sit[0] is False or self.player[1] is not None:
            for elem in text.split("\n"):
                text_surf = gui_font.render(elem, True, "#FFFFFF")
                self.screen.blit(text_surf, (self.x + width_scale(40, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                height += 25
        if self.player != [None, None] and Global_objects.is_selecting_sit[0]:
            if Global_objects.is_selecting_sit[1] == int(sitbutton.fonction[-1]):
                Global_objects.is_selecting_sit = [False, -1]