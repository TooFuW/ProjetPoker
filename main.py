#Menu du jeu Poker


import pygame, sys


class Button:
    """Classe Button pour créer des boutons dynamiques (https://www.youtube.com/watch?v=8SzTzvrWaAA)
    """

    def __init__(self, text : str, police : str, textsize : int, width : int, height : int, pos : tuple, elevation : int):
        """Initialisation de la classe Button

        Args:
            text (str): Texte d'affichage du bouton
            police (str): Police d'affichage du texte (seulement parmis les polices système disponibles)
            textsize (int): Taille du texte
            width (int): Largeur du bouton
            height (int): Hauteur du bouton
            pos (tuple): Position contenant deux valeurs x et y dans un tuple
            elevation (int): /!\ PLUS QUE 6 N'EST PAS RECOMMANDE /!\ Hauteur du bouton comparé au "sol" (purement cosmétique, pour donner un style "d'appui") (risque de bug si on appuie à un endroit qui ne va plus être le bouton lorsque celui-ci va se baisser)
        """
        # Attributs principaux
        self.pressed = False
        # self.elevation sert à garder la valeur par défaut de l'élévation, on va plutôt utiliser self.dynamic_elevation dans le code
        self.elevation = elevation
        self.dynamic_elevation = elevation
        # On garde la valeur y de pos pour que le mouvement du bouton reste aligné
        self.original_y_pos = pos[1]

        # Top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = "#475F77"

        # Bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = "#354B5E"

        # Button text
        gui_font = pygame.font.SysFont(police, textsize)
        self.text_surf = gui_font.render(text, True, "#FFFFFF")
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    
    def draw(self):
        """Génération/affichage du bouton
        """
        # Elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        # Affichage de "l'ombre" du bouton qui est sur le "sol"
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius = 10)
        # Affichage du bouton à cliquer
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius = 10)
        screen.blit(self.text_surf, self.text_rect)
        # On appelle constamment check_click pour vérifier si l'utilisateur interagit avec le bouton
        self.check_click()

    def check_click(self):
        """Vérifie si l'utilisateur clique sur le bouton pour faire l'action souhaitée
        """
        # On récupére la position de la souris
        mouse_pos = pygame.mouse.get_pos()
        # On vérifie si la position de la souris est sur le bouton
        if self.top_rect.collidepoint(mouse_pos):
            #On change la couleur du bouton lorsque la souris est dessus
            self.top_color = "#D74B4B"
            # On vérifie si l'utilisateur clique sur le clic gauche ([0] = gauche, [1] = molette, [2] = droit)
            if pygame.mouse.get_pressed()[0]:
                # On anime le bouton et change son état
                self.dynamic_elevation = 0
                self.pressed = True
            # On fait les actions souhaitées lorsque le clic est relaché
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    # CODE POUR QUAND LE BOUTON EST CLIQUE
                    print("click")
                    self.pressed = False
        # Le else est là pour reset l'état du bouton lorsqu'il n'y a plus aucune interaction
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = "#475F77"
            self.pressed = False


# Pygame setup
pygame.init()
# Taille de la fenêtre
screen = pygame.display.set_mode((1600, 1024))
# Nom de la fenêtre
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

# Chargement de l'image de fond
fond = pygame.image.load("PokerBackground.jpg")
fond = pygame.transform.scale(fond, (1600, 1024))

#Création de l'objet accountbutton
accountbutton = Button("ACCOUNT", "Roboto", 20, 150, 75, (1425, 25), 3)
# Création de l'objet playbutton
playbutton = Button("PLAY", "Roboto", 100, 425, 100, (600, 400), 6)
# Création de l'objet settingsbutton
settingsbutton = Button("SETTINGS", "Roboto", 100, 425, 100, (600, 550), 6)
# Création de l'objet quitbutton
exitbutton = Button("EXIT", "Roboto", 100, 425, 100, (600, 700), 6)

# Gameloop
while True:
    # Rassemblement de tout les événements
    for event in pygame.event.get():
        # pygame.QUIT event veut dire que l'utilisateur a cliqué sur la croix pour fermer la fenêtre
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Dessin l'image de fond sur la surface de l'écran
    screen.blit(fond, (0, 0))

    # Affichage des bouttons
    accountbutton.draw()
    playbutton.draw()
    settingsbutton.draw()
    exitbutton.draw()

    # Met à jour l'affichage de l'interface
    pygame.display.update()

    #Limite les FPS à 60
    clock.tick(60)


















#fonction importante pour plus tard à laisser en bas 
def str_to_list(string: str):   #fonctionne seulement sur une liste supposée valide
    liste = []
    string = string.removeprefix("[")
    string = string.removesuffix("]")

    return string.split(",")