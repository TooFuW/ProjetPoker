#Menu du jeu Poker


import pygame
import sys


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


class ScrollBox:
    """Classe ScrollBox pour créer des ScrollSox (classe compliquée, pas bien écrite mais fonctionne donc éviter de modifier xD)
    """

    def __init__(self, x : int, y : int, width : int, height : int, servers : list):
        """Initialisation de la classe ScrollBox

        Args:
            x (int): Position x de la scrollbox
            y (int): Position y de la scrollbox
            width (int): Largeur de la scrollbox
            height (int): Hauteur de la scrollbox
            servers (list): Liste des serveurs/tables à afficher
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.servers = servers
        self.scroll_pos = 0
        self.indentation = "                    "
        self.hauteurbox = 50

    def draw(self):
        """Génération/affichage de la scrollbox
        """
        # Créez une surface transparente
        transparent_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Dessinez le rectangle transparent sur la surface
        pygame.draw.rect(transparent_surface, (0, 0, 0, 128), (0, 0, self.width, self.height))
        
        # Blittez la surface transparente sur l'écran
        screen.blit(transparent_surface, (self.x, self.y))

        # Calcul de la zone d'affichage des éléments
        display_area = pygame.Rect(self.x, self.y, self.width, self.height)

        # Décalage initial
        item_offset_y = 0

        # Dessin des éléments visibles
        for i, server in enumerate(self.servers[self.scroll_pos:]):
            item_y = self.y + item_offset_y
            # Délimitation de la zone de la scrollbox
            item_rect = Button((server[0] + self.indentation + "Size of the table : " + str(server[1])), "Roboto", 24, self.width, self.hauteurbox, (self.x, item_y), 3)
            item_rect.check_click()
            # Affichage des serveurs disponibles
            if item_rect.top_rect.colliderect(display_area):
                item_rect.draw()
            # Ajouter un padding entre chaque serveur
            item_offset_y += self.hauteurbox + 10  # Ajouter 5 pixels de padding

    def scroll_up(self):
        """Pour scroller vers le haut
        """
        if self.scroll_pos > 0:
            self.scroll_pos -= 1

    def scroll_down(self):
        """Pour scroller vers le bas
        """
        # IMPORTANT : 45 doit être égal à item_offset_y sinon ca ne marchera pas !
        if self.scroll_pos < len(self.servers) - (self.height // 60):
            self.scroll_pos += 1


class HUD_State:
    """Classe HUD_State créée pour gérer l'interface active (https://www.youtube.com/watch?v=j9yMFG3D7fg)
    """

    def __init__(self):
        """Initialisation de l'état de l'interface
        """
        # self.state définit l'état actuel de l'interface (qui est par défaut Main Menu)
        self.state = "Main Menu"
        self.lobbyycreated = False
    
    def mainmenu(self):
        """mainmenu est la fonction qui fait tourner/afficher le menu principal
        """
        # Rassemblement de tout les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Dessine l'image de fond sur la screen de l'écran (IMPORANT CAR SE SUPERPOSE A L'INTERFACE PRECEDENT ET PERMET DE "L'EFFACER")
        screen.blit(fond, (0, 0))
        # Dessine le logo du jeu
        logojeu = pygame.image.load("PokerBackground.jpg")
        logojeu = pygame.transform.scale(logojeu, (250, 250))
        screen.blit(logojeu, ((screen_width // 2) - 125, 25))
        # Dessine le logo MWTE
        logomwte = pygame.image.load("logo mwte.jpg")
        logomwte = pygame.transform.scale(logomwte, (150, 150))
        screen.blit(logomwte, (25, screen_height - 160))

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
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Molette de la souris vers le haut
                    scrollbox.scroll_up()
                elif event.button == 5:  # Molette de la souris vers le bas
                    scrollbox.scroll_down()

        # Dessine l'image de fond sur la screen de l'écran
        screen.blit(fond, (0, 0))
        # Affichage du titre de la page en haut à gauche
        gui_font = pygame.font.SysFont("Roboto", 50, False, True)
        text_surf = gui_font.render("Table List", True, "#FFFFFF")
        text_rect = text_surf.get_rect(center = pygame.Rect((30, 0), (150, 75)).center)
        screen.blit(text_surf, text_rect)

        # Dessin de la scrollbox
        scrollbox.draw()

        # Affichage des bouttons
        # Cliquer sur le bouton BACK ferme la fenêtre purement et simplement
        backbutton.draw()
        # Cliquer sur le bouton CREER TABLE crée une nouvelle table
        createtablebutton.draw()

        # Met à jour l'affichage de l'interface
        pygame.display.update()
    
    def settingmenu(self):
        """settingmenu est la fonction qui fait tourner/afficher le menu des settings
        """
        # Rassemblement de tout les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Dessine l'image de fond sur la screen de l'écran (IMPORANT CAR SE SUPERPOSE A L'INTERFACE PRECEDENT ET PERMET DE "L'EFFACER")
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
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Dessine l'image de fond sur la screen de l'écran (IMPORANT CAR SE SUPERPOSE A L'INTERFACE PRECEDENT ET PERMET DE "L'EFFACER")
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
            self.lobbyycreated = False
            self.mainmenu()
        elif self.state == "Lobby Menu":
            self.lobbymenu()
        elif self.state == "Setting Menu":
            self.lobbyycreated = False
            self.settingmenu()
        elif self.state == "Account Menu":
            self.lobbyycreated = False
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

# Récupération de la liste des lobbys disponibles et de leurs informations
server_list = [["Table 1", 15], ["Table 2", 10], ["Table 3", 20], ["Table 4", 5], ["Table 5", 8], ["Table 6", 8], ["Table 7", 11], ["Table 8", 18], ["Table 9", 12], ["Table 10", 3], ["Table 11", 15], ["Table 12", 10], ["Table 13", 20], ["Table 14", 5], ["Table 15", 8], ["Table 16", 8], ["Table 17", 11], ["Table 18", 18], ["Table 19", 12], ["Table 20", 3]]

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
backbutton = Button("BACK", "Roboto", 100, 425, 100, ((screen_width // 2)-(425//2), (screen_height // 2) + 400), 6)
# Création de l'objet createtablebutton
createtablebutton = Button("CREATE TABLE", "Roboto", 70, 425, 100, ((screen_width - 500), (screen_height //2 - 300)), 6)

# Création de l'objet scrollbox 
scrollbox = ScrollBox(((screen_width/2)/2)/4, 150, screen_width/2 + ((screen_width/2)/2)/2, screen_height/2 + (screen_height/2)/3, server_list)

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