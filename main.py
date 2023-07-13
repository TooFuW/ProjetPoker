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
        self.text = text
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
        gui_font = pygame.font.SysFont(police, textsize, False, False)
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
                # CODE POUR QUAND LE BOUTON EST CLIQUE
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                    if self.text == "PLAY":
                        game_state.state = "Lobby Menu"
                    elif self.text == "SETTINGS":
                        game_state.state = "Setting Menu"
                    elif self.text == "ACCOUNT":
                        game_state.state = "Account Menu"
                    elif self.text == "EXIT":
                        pygame.quit()
                        sys.exit()
                    elif self.text == "BACK":
                        game_state.state = "Main Menu"
        # Le else est là pour reset l'état du bouton lorsqu'il n'y a plus aucune interaction
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = "#475F77"
            self.pressed = False


class HUD_State:
    """Classe HUD_State créée pour gérer l'interface active (https://www.youtube.com/watch?v=j9yMFG3D7fg)
    """

    def __init__(self):
        """Initialisation de l'état de l'interface
        """
        # self.state définit l'état actuel de l'interface (qui est par défaut Main Menu)
        self.state = "Main Menu"
    
    def mainmenu(self):
        """mainmenu est la fonction qui fait tourner/afficher le menu principal
        """
        # Rassemblement de tout les événements
        for event in pygame.event.get():
            pass

        # Dessine l'image de fond sur la surface de l'écran (IMPORANT CAR SE SUPERPOSE A L'INTERFACE PRECEDENT ET PERMET DE "L'EFFACER")
        screen.blit(fond, (0, 0))
        # Dessine le logo du jeu
        logopoker = pygame.transform.scale(pokertablebackground, (250, 250))
        screen.blit(logopoker, (screen_height//2 + 200, 75))
        # Dessine le logo MWTE
        logomwte = pygame.transform.scale(pokertablebackground, (150, 150))
        screen.blit(logomwte, (25 , screen_width//2 - 75))

        # Affichage des bouttons
        # Cliquer sur le bouton PLAY ouvre l'interface présentant les lobbys disponibles
        playbutton.draw()
        # Cliquer sur le bouton SETTINGS ouvre l'interface présentant les paramètres
        settingsbutton.draw()
        # Cliquer sur le bouton ACCOUNT ouvre l'interface présentant les informations du compte actif
        accountbutton.draw()
        # Cliquer sur le bouton EXIT ferme la fenêtre purement et simplement
        exitbutton.draw()

        # Met à jour l'affichage de l'interface
        pygame.display.update()
    
    def lobbymenu(self):
        """lobbymenu est la fonction qui fait tourner/afficher le menu des lobbys
        """
        # Rassemblement de tout les événements
        for event in pygame.event.get():
            pass

        # Dessine l'image de fond sur la surface de l'écran
        screen.blit(fond, (0, 0))
        # Affichage du titre de la page en haut à gauche
        gui_font = pygame.font.SysFont("Roboto", 50, False, True)
        text_surf = gui_font.render("Table List", True, "#FFFFFF")
        text_rect = text_surf.get_rect(center = pygame.Rect((30, 0), (150, 75)).center)
        screen.blit(text_surf, text_rect)

        # Affichage des bouttons
        # Cliquer sur le bouton BACK ferme la fenêtre purement et simplement
        backbutton.draw()

        # Met à jour l'affichage de l'interface
        pygame.display.update()
    
    def settingmenu(self):
        """settingmenu est la fonction qui fait tourner/afficher le menu des settings
        """
        # Rassemblement de tout les événements
        for event in pygame.event.get():
            pass

        # Dessine l'image de fond sur la surface de l'écran (IMPORANT CAR SE SUPERPOSE A L'INTERFACE PRECEDENT ET PERMET DE "L'EFFACER")
        screen.blit(fond, (0, 0))

        # Affichage du titre de la page en haut à gauche
        gui_font = pygame.font.SysFont("Roboto", 50, False, True)
        text_surf = gui_font.render("Settings Menu", True, "#FFFFFF")
        text_rect = text_surf.get_rect(center = pygame.Rect((70, 0), (150, 75)).center)
        screen.blit(text_surf, text_rect)

        # Affichage des bouttons
        # Cliquer sur le bouton BACK ferme la fenêtre purement et simplement
        backbutton.draw()

        # Met à jour l'affichage de l'interface
        pygame.display.update()
    
    def accountmenu(self):
        """accountmenu est la fonction qui fait tourner/afficher le menu du compte actif
        """
        # Rassemblement de tout les événements
        for event in pygame.event.get():
            pass

        # Dessine l'image de fond sur la surface de l'écran (IMPORANT CAR SE SUPERPOSE A L'INTERFACE PRECEDENT ET PERMET DE "L'EFFACER")
        screen.blit(fond, (0, 0))

        # Affichage du titre de la page en haut à gauche
        gui_font = pygame.font.SysFont("Roboto", 50, False, True)
        text_surf = gui_font.render("Your Account", True, "#FFFFFF")
        text_rect = text_surf.get_rect(center = pygame.Rect((50, 0), (150, 75)).center)
        screen.blit(text_surf, text_rect)

        # Affichage des bouttons
        # Cliquer sur le bouton BACK ferme la fenêtre purement et simplement
        backbutton.draw()

        # Met à jour l'affichage de l'interface
        pygame.display.update()

    def state_manager(self):
        """state_manager se charge d'afficher la bonne interface en fonction de l'état de l'interface
        """
        if self.state == "Main Menu":
            self.mainmenu()
        elif self.state == "Lobby Menu":
            self.lobbymenu()
        elif self.state == "Setting Menu":
            self.settingmenu()
        elif self.state == "Account Menu":
            self.accountmenu()


# Pygame setup
pygame.init()
game_state = HUD_State()
# Taille de la fenêtre
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
# Nom de la fenêtre
pygame.display.set_caption("Menu Jeu Poker")
clock = pygame.time.Clock()

# Chargement de l'image de fond
pokertablebackground = pygame.image.load("PokerBackground.jpg")
fond = pygame.transform.scale(pokertablebackground, (screen_width, screen_height))

# Création de tout les boutons utilisés
# Création de l'objet accountbutton
accountbutton = Button("ACCOUNT", "Roboto", 30, 150, 75, ((screen_width - 170), (20)), 3)
# Création de l'objet playbutton
playbutton = Button("PLAY", "Roboto", 100, 425, 100, ((screen_width // 2)-(425//2), (screen_height // 2) - 30), 6)
# Création de l'objet settingsbutton
settingsbutton = Button("SETTINGS", "Roboto", 100, 425, 100, ((screen_width // 2)-(425//2), (screen_height // 2) + 100), 6)
# Création de l'objet quitbutton
exitbutton = Button("EXIT", "Roboto", 100, 425, 100, ((screen_width // 2)-(425//2), (screen_height // 2) + 230), 6)
# Création de l'objet backbutton
backbutton = Button("BACK", "Roboto", 100, 425, 100, ((screen_width // 2)-(425//2), (screen_height // 2) + 230), 6)

# Gameloop
while True:
    # Chargement de la musique de fond et mise en boucle
    if pygame.mixer.music.get_busy() != True:
        pygame.mixer.music.load("mainmenu_soundtrack.mp3")
        pygame.mixer.music.rewind()
        pygame.mixer.music.play()
    # Cet appel permet de gérer l'interface active
    game_state.state_manager()
    # Limite les FPS à 60
    clock.tick(60)

































#fonction importante pour plus tard à laisser en bas 
def str_to_list(string: str):   #fonctionne seulement sur une liste supposée valide
    liste = []
    string = string.removeprefix("[")
    string = string.removesuffix("]")

    return string.split(",")