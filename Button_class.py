# Button Class


import pygame
from Screen_adaptation import *
from Check_click import *


class Button:
    """Classe Button pour créer des boutons dynamiques (https://www.youtube.com/watch?v=8SzTzvrWaAA)
    """

    def __init__(self, largeur_actuelle : int, hauteur_actuelle : int, screen : pygame.Surface, fonction : str, text : str, police : str, textsize : int, top_color : str or int, bottom_color : str or int, hovering_color : str or int, width : int, height : int, pos : tuple, elevation : int, round_border : int, image : str = None):
        """Initialisation de la classe Button

        Args:
            largeur_actuelle (int): Largeur de l'écran (pour width_scale())
            hauteur_actuelle (int): Hauteur de l'écran (pour height_scale())
            screen (pygame.Surface): Ecran sur lequel afficher la fenêtre (écran de l'utilisateur)
            fonction (str) : Usage de la fonction, à utiliser dans self.check_click pour lier des actions au bouton correspondant
            text (str): Texte d'affichage du bouton
            police (str): Police d'affichage du texte (seulement parmis les polices système disponibles)
            textsize (int): Taille du texte
            top_color (str or int): Couleur de la partie haute du bouton
            bottom_color (str or int): Couleur de la partie basse du bouton
            hovering_color (str or int): Couleur du bouton lorsque la souris est dessus
            width (int): Largeur du bouton
            height (int): Hauteur du bouton
            pos (tuple): Position contenant deux valeurs x et y dans un tuple
            elevation (int): /!\ PLUS QUE 6 N'EST PAS RECOMMANDE /!\ Hauteur du bouton comparé au "sol" (purement cosmétique, pour donner un style "d'appui") (risque de bug si on appuie à un endroit qui ne va plus être le bouton lorsque celui-ci va se baisser)
            round_border (int): Puissance de la courbure du bouton
            image (str) = None: Le lien relatif de l'image s'il y en a une comme fond du bouton (None par défaut)
        """
        # Attributs généraux
        self.pressed = False
        self.fonction = fonction
        self.courbure = round_border
        self.pos_x = width_scale(pos[0], largeur_actuelle)
        self.pos_y = height_scale(pos[1], hauteur_actuelle)
        self.pos = (self.pos_x, self.pos_y)
        self.hovering_color = hovering_color
        self.largeur_actuelle = largeur_actuelle
        self.hauteur_actuelle = hauteur_actuelle
        self.screen = screen
        # Pour savoir si on peut modifier ou non les paramètres du compte
        self.account_modifiable = False

        # self.elevation sert à garder la valeur par défaut de l'élévation, on va plutôt utiliser self.dynamic_elevation dans le code
        self.elevation = elevation
        self.dynamic_elevation = elevation
        # On garde la valeur y de pos pour que le mouvement du bouton reste aligné
        self.original_y_pos = self.pos_y

        # Top rectangle
        self.top_rect = pygame.Rect(self.pos, (width_scale(width, largeur_actuelle), height_scale(height, hauteur_actuelle)))
        self.top_color = top_color
        self.initial_top_color = top_color

        # Bottom rectangle
        self.bottom_rect = pygame.Rect(self.pos, (width_scale(width, largeur_actuelle), height_scale(elevation, hauteur_actuelle)))
        self.bottom_color = bottom_color

        # Button text
        self.text = text
        gui_font = pygame.font.SysFont(police, width_scale(textsize, largeur_actuelle), False, False)
        self.text_surf = gui_font.render(text, True, "#FFFFFF")
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

        # Button image
        self.image = None
        if image != None:
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, (width_scale(width, largeur_actuelle), height_scale(height, hauteur_actuelle)))

    def draw(self):
        """Génération/affichage du bouton
        """
        # Elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        # Affichage de "l'ombre" du bouton qui est sur le "sol"
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        pygame.draw.rect(self.screen, self.bottom_color, self.bottom_rect, border_radius = self.courbure)
        # Affichage du bouton à cliquer
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius = self.courbure)
        if self.image != None:
            self.screen.blit(self.image, self.top_rect)
        self.screen.blit(self.text_surf, self.text_rect)
        # On appelle constamment check_click pour vérifier si l'utilisateur interagit avec le bouton
        self.check_click()

    def check_click(self):
        """Vérifie si l'utilisateur clique sur le bouton pour faire l'action souhaitée
        """
        # On récupére la position de la souris
        mouse_pos = pygame.mouse.get_pos()
        # On vérifie si la position de la souris est sur le bouton
        if self.top_rect.collidepoint(mouse_pos):
            # On change la couleur du bouton lorsque la souris est dessus
            self.top_color = self.hovering_color
            # On vérifie si l'utilisateur clique sur le clic gauche ([0] = gauche, [1] = molette, [2] = droit)
            if pygame.mouse.get_pressed()[0]:
                # On anime le bouton et change son état
                self.dynamic_elevation = 0
                self.pressed = True
            # On fait les actions souhaitées lorsque le clic est relaché
            else:
                # CODE POUR QUAND LE BOUTON EST CLIQUE
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                    check_click(self)
        # Le else est là pour reset l'état du bouton lorsqu'il n'y a plus aucune interaction
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = self.initial_top_color
            self.pressed = False