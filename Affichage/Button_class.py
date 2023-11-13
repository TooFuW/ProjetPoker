"""Document contenant la classe Button où sont définis les boutons"""


import pygame
from Screen_adaptation import *
import Check_click


class Button:
    """Classe Button pour créer des boutons dynamiques (https://www.youtube.com/watch?v=8SzTzvrWaAA)
    """

    def __init__(self, largeur_actuelle : int, hauteur_actuelle : int, screen : pygame.Surface, fonction : str, text : str, police : str, textsize : int, color : tuple, hovering_color : tuple, clicking_color : tuple, width : int, height : int, pos : tuple, round_border : int, image : str = None):
        """Initialisation de la classe Button

        Args:
            largeur_actuelle (int): Largeur de l'écran (pour width_scale())
            hauteur_actuelle (int): Hauteur de l'écran (pour height_scale())
            screen (pygame.Surface): Ecran sur lequel afficher la fenêtre (écran de l'utilisateur)
            fonction (str) : Usage de la fonction, à utiliser dans self.check_click pour lier des actions au bouton correspondant
            text (str): Texte d'affichage du bouton
            police (str): Police d'affichage du texte (seulement parmis les polices système disponibles)
            textsize (int): Taille du texte
            color (tuple): Couleur de la partie haute du bouton
            hovering_color (tuple): Couleur du bouton lorsque la souris est dessus
            clicking_color (tuple): Couleur du bouton lorsque la souris clique dessus
            width (int): Largeur du bouton
            height (int): Hauteur du bouton
            pos (tuple): Position contenant deux valeurs x et y (x : largeur, y : hauteur)
            round_border (int): Puissance de la courbure des bords du bouton
            image (str) = None: Le lien relatif de l'image s'il y en a une comme fond du bouton
        """
        # Attributs généraux
        self.pressed = False
        # self.pressed différent de self.is_pressing, ce dernier sert à savoir si le bouton est simplement cliqué quand le premier sert pour gérer les interactions dans la classe
        self.is_pressing = False
        self.fonction = fonction
        self.largeur_actuelle = largeur_actuelle
        self.hauteur_actuelle = hauteur_actuelle
        self.width = width_scale(width, largeur_actuelle)
        self.height = height_scale(height, self.hauteur_actuelle)
        self.pos_x = width_scale(pos[0], largeur_actuelle)
        self.pos_y = height_scale(pos[1], hauteur_actuelle)
        self.pos = (self.pos_x, self.pos_y)
        self.screen = screen
        # Pour savoir si on peut modifier ou non les paramètres du compte
        self.account_modifiable = False
        self.button_interactible = True

        # On garde la valeur y de pos pour que le mouvement du bouton reste aligné
        self.original_y_pos = self.pos_y

        # Button rectangle
        self.button_rect = pygame.Rect(self.pos, (self.width, self.height))
        self.courbure = width_scale(round_border, self.largeur_actuelle, True)
        # Couleurs sous forme (w, x, y, z) où w, x et y sont les couleurs RGB et z la force de transparence (de 0 à 255)
        self.color = color
        self.initial_color = color
        self.hovering_color = hovering_color
        self.clicking_color = clicking_color

        # Button text
        self.text = text
        gui_font = pygame.font.SysFont(police, width_scale(textsize, self.largeur_actuelle, True), False, False)
        self.text_surf = gui_font.render(self.text, True, "#FFFFFF")
        self.text_rect = self.text_surf.get_rect(center = self.button_rect.center)

        # Button image
        self.image = None
        if image != None:
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self):
        """Génération/affichage du bouton
        """
        # Affichage du bouton à cliquer
        transparent_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, self.color, (0, 0, self.width, self.height), border_radius = self.courbure)
        self.screen.blit(transparent_surface, (self.pos_x, self.pos_y))
        pygame.draw.rect(self.screen, (0,0,0), (self.pos_x, self.pos_y, self.width, self.height), width_scale(3, self.largeur_actuelle, True), self.courbure)
        if self.image != None:
            self.screen.blit(self.image, self.button_rect)
        self.screen.blit(self.text_surf, self.text_rect)
        # On appelle constamment check_click pour vérifier si l'utilisateur interagit avec le bouton seulement si l'utilisateur peut interagir avec
        self.check_click()

    def check_click(self):
        """Vérifie si l'utilisateur clique sur le bouton pour faire l'action souhaitée
        """
        # On récupére la position de la souris
        mouse_pos = pygame.mouse.get_pos()
        # On vérifie si la position de la souris est sur le bouton
        if self.button_rect.collidepoint(mouse_pos):
            if self.button_interactible:
                # On change la couleur du bouton lorsque la souris est dessus
                self.color = self.hovering_color
                # On vérifie si l'utilisateur clique sur le clic gauche ([0] = gauche, [1] = molette, [2] = droit)
                if pygame.mouse.get_pressed()[0]:
                    # On anime le bouton et change son état
                    self.pressed = True
                    self.is_pressing = True
                    self.color = self.clicking_color
                # On fait les actions souhaitées lorsque le clic est relaché
                else:
                    # CODE POUR QUAND LE BOUTON EST CLIQUE
                    if self.pressed:
                        self.pressed = False
                        Check_click.check_click(self)
                    if self.is_pressing:
                        self.is_pressing = False
        # Le else est là pour reset l'état du bouton lorsqu'il n'y a plus aucune interaction
        else:
            self.color = self.initial_color
            self.pressed = False