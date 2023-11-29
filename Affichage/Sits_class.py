"""Document contenant la classe Sits qui crée des sièges sur lesquels les joueurs peuvent s'asseoir, siège qui stocke alors les données de ce joueur qui est lié à ce siège pour la partie"""


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
        # Une liste contenant toutes les infos du joueur assi sur ce siège [sit_id, idplayer, pseudo, chips, link]
        self.player = [None, None]
        self.profile_picture = pygame.transform.scale(profile_picture, (width_scale(120, largeur_actuelle), height_scale(120, hauteur_actuelle)))
        self.selected = False
        # Référencement du siège sélectionné
        self.sit_selected = None
        # Variable pour savoir le temps restant au joueur pour parler et ainsi l'afficher
        self.temps_pourcent = 0
        # Variables pour gérer les animations des cartes
        self.pos_card1_x_arrive = self.x + width_scale(40, self.largeur_actuelle)
        self.pos_card1_y_arrive = self.y - height_scale(100, self.hauteur_actuelle)
        self.pos_card2_x_arrive = self.x + width_scale(140, self.largeur_actuelle)
        self.pos_card2_y_arrive = self.y - height_scale(100, self.hauteur_actuelle)
        self.pos_card1_x_actuel = width_scale(930, self.largeur_actuelle)
        self.pos_card1_y_actuel = height_scale(490, self.hauteur_actuelle)
        self.pos_card2_x_actuel = width_scale(930, self.largeur_actuelle)
        self.pos_card2_y_actuel = height_scale(490, self.hauteur_actuelle)
        self.pas_x = self.pos_card1_x_arrive - width_scale(930, self.largeur_actuelle)
        self.pas_y = self.pos_card1_y_arrive - height_scale(490, self.hauteur_actuelle)
   
    def draw(self):
        """Génération/affichage du siège
        """
        gui_font = pygame.font.SysFont("Roboto", width_scale(30, self.largeur_actuelle, True))
        # Affichage du fond du widget de siège
        # On affiche le bouton pour s'asseoir si le joueur n'est pas encore assis
        if Global_objects.is_selecting_sit[0] and self.player[1] is None and not Global_objects.game_started:
            sitbutton = Button(self.largeur_actuelle, self.hauteur_actuelle, self.screen, f"sit {self.player[0] + 1}", f"Sit down [{self.player[0] + 1}]", "Roboto", 30, (255, 255, 255), (0, 0, 0, 180), (50, 50, 50, 200), (90, 90, 90, 180), (0, 0, 0), 3, (self.width * 1920) // self.largeur_actuelle, (self.height * 1080) // self.hauteur_actuelle, ((self.x * 1920) // self.largeur_actuelle, (self.y * 1080) // self.hauteur_actuelle), 50)
            sitbutton.check_click()
            sitbutton.draw()
            mouse_pos = pygame.mouse.get_pos()
            # Quand le bouton de siège est cliqué
            if sitbutton.button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    self.selected = True
                    self.sit_selected = sitbutton
                else:
                    if self.selected:
                        self.selected = False
                        check_click(self.sit_selected)
        # Sinon on affiche directement les infos du siège
        else:
            # On dessine les cartes du joueur s'il est le client sinon on met des dos de cartes
            if Global_objects.client_actuel == self.player[0] + 1:
                if Global_objects.nombre_cartes > 0:
                    card1 = pygame.transform.scale(Global_objects.cards[Global_objects.card_1], (width_scale(70, self.largeur_actuelle), height_scale(110, self.hauteur_actuelle)))
                if Global_objects.nombre_cartes > 1:
                    card2 = pygame.transform.scale(Global_objects.cards[Global_objects.card_2], (width_scale(70, self.largeur_actuelle), height_scale(110, self.hauteur_actuelle)))
            else:
                if Global_objects.nombre_cartes > 0:
                    card1 = pygame.transform.scale(Global_objects.cards["dos"], (width_scale(70, self.largeur_actuelle), height_scale(110, self.hauteur_actuelle)))
                if Global_objects.nombre_cartes > 1:
                    card2 = pygame.transform.scale(Global_objects.cards["dos"], (width_scale(70, self.largeur_actuelle), height_scale(110, self.hauteur_actuelle)))
            if Global_objects.nombre_cartes > 0:
                self.screen.blit(card1, (self.x + width_scale(40, self.largeur_actuelle), self.y - height_scale(100, self.hauteur_actuelle), width_scale(0, self.largeur_actuelle), height_scale(0, self.hauteur_actuelle)))
            if Global_objects.nombre_cartes > 1:
                self.screen.blit(card2, (self.x + width_scale(140, self.largeur_actuelle), self.y - height_scale(100, self.hauteur_actuelle), width_scale(0, self.largeur_actuelle), height_scale(0, self.hauteur_actuelle)))
            # On affiche le fond transparent du widget du siège
            transparent_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(transparent_surface, (0, 0, 0, 160), (0, 0, self.width, self.height), border_radius = 50)
            self.screen.blit(transparent_surface, (self.x, self.y))
            # On affiche la pdp du joueur
            self.screen.blit(self.profile_picture, (self.x - width_scale(65, self.largeur_actuelle), self.y - height_scale(22, self.hauteur_actuelle)))
            # On affiche un petit rond pour la zone où l'on va afficher la mise
            pygame.draw.circle(self.screen, "#475F77", (self.x + self.width, self.y + (self.height/2)), width_scale(25, self.largeur_actuelle))
            if Global_objects.game_bets[self.player[0]] is None:
                text_surf = gui_font.render(f"0", True, "#FFFFFF")
            else:
                text_surf = gui_font.render(f"{Global_objects.game_bets[self.player[0]]}", True, "#FFFFFF")
            text_rect = text_surf.get_rect(center = (self.x + self.width, self.y + (self.height/2)))
            self.screen.blit(text_surf, text_rect)
            # On affiche les barre qui représentent le temps restant au joueur pour parler
            # Barre blanche du fond
            pygame.draw.rect(self.screen, "#FFFFFF", pygame.Rect((self.x + width_scale(35, self.largeur_actuelle), self.y + self.height - height_scale(20, self.hauteur_actuelle)), (self.width - width_scale(70, self.largeur_actuelle), height_scale(10, self.hauteur_actuelle))), border_radius = 10)
            # Barre de remplissage
            pygame.draw.rect(self.screen, "#FF0000", pygame.Rect((self.x + width_scale(35, self.largeur_actuelle), self.y + self.height - height_scale(20, self.hauteur_actuelle)), (width_scale(self.temps_pourcent, self.largeur_actuelle), height_scale(10, self.hauteur_actuelle))), border_radius = 10)
            if Global_objects.game_started and Global_objects.parole == self.player[0] + 1:
                self.temps_pourcent = int((self.width - width_scale(70, self.largeur_actuelle)) * Global_objects.game_state.timer[0] / 15)
        # Affichage des infos du joueur du siège actuel par dessus la surface transparente
        if self.player[1] is None:
            text = "Sit Available"
        else:
            text = f"{self.player[1]}\n{self.player[2]}"
            text = text.replace("'", "")
        height = height_scale(10, self.hauteur_actuelle)
        if not Global_objects.is_selecting_sit[0] or self.player[1] is not None:
            for elem in text.split("\n"):
                text_surf = gui_font.render(elem, True, "#FFFFFF")
                self.screen.blit(text_surf, (self.x + width_scale(40, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                height += height_scale(25, self.hauteur_actuelle)