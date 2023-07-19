#Menu du jeu Poker


import pygame
import sys
import webbrowser


class Button:
    """Classe Button pour créer des boutons dynamiques (https://www.youtube.com/watch?v=8SzTzvrWaAA)
    """

    def __init__(self, fonction : str, text : str, police : str, textsize : int, width : int, height : int, pos : tuple, elevation : int, image : str = None):
        """Initialisation de la classe Button

        Args:
            text (str): Texte d'affichage du bouton
            police (str): Police d'affichage du texte (seulement parmis les polices système disponibles)
            textsize (int): Taille du texte
            width (int): Largeur du bouton
            height (int): Hauteur du bouton
            pos (tuple): Position contenant deux valeurs x et y dans un tuple
            elevation (int): /!\ PLUS QUE 6 N'EST PAS RECOMMANDE /!\ Hauteur du bouton comparé au "sol" (purement cosmétique, pour donner un style "d'appui") (risque de bug si on appuie à un endroit qui ne va plus être le bouton lorsque celui-ci va se baisser)
            image (str) (None par défaut): Le lien relatif de l'image s'il y en a une comme fond du bouton (None par défaut)
        """
        # Attributs généraux
        self.pressed = False
        self.fonction = fonction

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
        self.text = text
        gui_font = pygame.font.SysFont(police, textsize, False, False)
        self.text_surf = gui_font.render(text, True, "#FFFFFF")
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

        # Button image
        self.image = None
        if image != None:
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, (width, height))

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
        if self.image != None:
            screen.blit(self.image, self.top_rect)
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
            # On change la couleur du bouton lorsque la souris est dessus
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
                    if self.fonction == "play":
                        game_state.state = "Lobby Menu"
                    elif self.fonction == "settings":
                        game_state.state = "Setting Menu"
                    elif self.fonction == "account":
                        game_state.state = "Account Menu"
                    elif self.fonction == "exit":
                        pygame.quit()
                        sys.exit()
                    elif self.fonction == "back":
                        game_state.state = "Main Menu"
                    elif self.fonction == "history":
                        game_state.state = "History Menu"
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
        self.indentation = "          "# Len = 10
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
            text = (server[0] + self.indentation + str(server[1]) + self.indentation + server[2] + self.indentation + server[3] + self.indentation + server[4] + self.indentation + server[5])
            item_rect = Button("scrollbox", text , "Roboto", 24, self.width, self.hauteurbox, (self.x, item_y), 3)
            item_rect.check_click()
            # Affichage des serveurs disponibles
            if item_rect.top_rect.colliderect(display_area):
                item_rect.draw()
            # Ajouter un padding entre chaque serveur
            item_offset_y += self.hauteurbox + 10  # Ajouter 10 pixels de padding

    def scroll_up(self):
        """Pour scroller vers le haut
        """
        if self.scroll_pos > 0:
            self.scroll_pos -= 1

    def scroll_down(self):
        """Pour scroller vers le bas
        """
        if self.scroll_pos < (len(self.servers) - 1) - (self.height // (self.hauteurbox + 10)):
            self.scroll_pos += 1


class HUD_State:
    """Classe HUD_State créée pour gérer l'interface active (https://www.youtube.com/watch?v=j9yMFG3D7fg)
    """

    def __init__(self):
        """Initialisation de l'état de l'interface
        """
        # self.state définit l'état actuel de l'interface (qui est par défaut Main Menu)
        self.state = "Main Menu"
        self.is_pressing_logomwte = False
    
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
        screen.blit(logojeu, ((screen_width // 2) - (250 // 2), (screen_height // 2) - (1000 // 2)))
        # Dessine le logo MWTE
        screen.blit(logomwte, logomwte_rect)

        # On récupére la position de la souris
        mouse_pos = pygame.mouse.get_pos()
        # On vérifie si la position de la souris est sur le bouton
        if logomwte_rect.collidepoint(mouse_pos):
            gui_font = pygame.font.SysFont("Roboto", 20, False, True)
            text_surf = gui_font.render("Aller sur le site officiel MWTE", True, "#000000")
            pygame.draw.rect(screen, "#FFFFFF", pygame.Rect((mouse_pos[0], mouse_pos[1] + 15), (200, 20)))
            screen.blit(text_surf, (mouse_pos[0], mouse_pos[1] + 20))
            if pygame.mouse.get_pressed()[0]:
                self.is_pressing_logomwte = True
            else:
                if self.is_pressing_logomwte == True:
                    self.is_pressing_logomwte = False
                    webbrowser.open("https://mwtestudio.wixsite.com/mwte-studio")

        # Affichage des bouttons
        # Cliquer sur le bouton PLAY ouvre l'interface présentant les lobbys disponibles
        playbutton.draw()
        # Cliquer sur le bouton SETTINGS ouvre l'interface présentant les paramètres
        settingsbutton.draw()
        # Cliquer sur le bouton ACCOUNT ouvre l'interface présentant les informations du compte actif
        accountbutton.draw()
        # Cliquer sur le bouton EXIT ferme la fenêtre purement et simplement
        exitbutton.draw()
        # Cliquer sur le bouton GAMES HISTORY affiche l'historique des parties
        gamehistorybutton.draw()

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

    def historymenu(self):
        """historymenu est la fonction qui fait tourner/afficher le menu de l'historique des parties du compte actif
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
        text_surf = gui_font.render("Games History", True, "#FFFFFF")
        text_rect = text_surf.get_rect(center = pygame.Rect((60, 0), (150, 75)).center)
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
        elif self.state == "History Menu":
            self.historymenu()


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

# Récupération de la liste des lobbys disponibles et de leurs informations ([0] = Nom de la table, [1] = Nombre de joueurs/nombre de joueurs max, [2] = Montant de la mise, [3] = Pot moyen, [4] = Tapis moyen)
server_list = [["Table 1", "0/5", "50/100", "15K", "25K", "ID1"], ["Table 2", "1/6", "50/100", "10K", "20K", "ID2"], ["Table 3", "2/7", "50/100", "20K", "30K", "ID3"], ["Table 4", "3/8", "50/100", "5K", "15K", "ID4"], ["Table 5", "4/9", "50/100", "8K", "18K", "ID5"], ["Table 6", "5/9", "50/100", "8K", "18K", "ID6"], ["Table 7", "6/9", "50/100", "11K", "21K", "ID7"], ["Table 8", "7/9", "50/100", "18K", "28K", "ID8"], ["Table 9", "8/9", "50/100", "12K", "22K", "ID9"], ["Table 10", "9/9", "50/100", "3K", "13K", "ID10"], ["Table 11", "0/6", "50/100", "15K", "25K", "ID11"], ["Table 12", "1/7", "50/100", "10K", "20K", "ID12"], ["Table 13", "2/8", "50/100", "20K", "30K", "ID13"], ["Table 14", "3/9", "50/100", "5K", "15K", "ID14"], ["Table 15", "4/9", "50/100", "8K", "18K", "ID15"], ["Table 16", "5/9", "50/100", "8K", "18K", "ID16"], ["Table 17", "6/9", "50/100", "11K", "21K", "ID17"], ["Table 18", "7/9", "50/100", "18K", "28K", "ID18"], ["Table 19", "8/9", "50/100", "12K", "22K", "ID19"], ["Table 20", "9/9", "50/100", "3K", "13K", "ID20"]]

# Chargement de l'image de fond
pokertablebackground = pygame.image.load("PokerBackground.jpg")
fond = pygame.transform.scale(pokertablebackground, (screen_width, screen_height))

# Chargement du logo du jeu
logojeu = pygame.image.load("PokerBackground.jpg")
logojeu = pygame.transform.scale(logojeu, (250, 250))

# Chargement du logo MWTE
logomwte = pygame.image.load("logo mwte.jpg")
logomwte = pygame.transform.scale(logomwte, (175, 175))
logomwte_rect = logomwte.get_rect()
logomwte_rect.topleft = ((screen_width // 2) - (1900 // 2), (screen_height // 2) + (700 // 2))

# Création de tout les boutons utilisés
# Création de l'objet accountbutton
accountbutton = Button("account", "ACCOUNT", "Roboto", 30, 150, 75, ((screen_width // 2) + (1600 // 2), (screen_height // 2) - (1050 // 2)), 3)
# Création de l'objet playbutton
playbutton = Button("play", "PLAY", "Roboto", 150, 500, 500, ((screen_width // 2) - (500 // 2), (screen_height // 2) - (350 // 2)), 6)
# Création de l'objet settingsbutton
settingsbutton = Button("settings", "SETTINGS", "Roboto", 70, 300, 500, ((screen_width // 2) - (1300 // 2), (screen_height // 2) - (350 // 2)), 6)
# Création de l'objet quitbutton
exitbutton = Button("exit", "EXIT", "Roboto", 70, 425, 100, ((screen_width // 2) - (425 // 2), (screen_height // 2) + (800 // 2)), 6)
# Création de l'objet backbutton
backbutton = Button("back", "", "Roboto", 70, 200, 200, ((screen_width // 2)-(200 // 2), (screen_height // 2) + (600 // 2)), 6, "backarrow.png")
# Création de l'objet createtablebutton
createtablebutton = Button("create table", "CREATE TABLE", "Roboto", 70, 425, 100, ((screen_width // 2) + (900 // 2), (screen_height // 2) - (700 // 2)), 6)
# Créaion de l'objet gamehistorybutton
gamehistorybutton = Button("history", "HISTORY", "Roboto", 70, 300, 500, ((screen_width // 2) + (700 // 2), (screen_height // 2) - (350 // 2)), 6)

# Création de l'objet scrollbox 
scrollbox = ScrollBox((screen_width // 2) - (1800 // 2), (screen_height // 2) - (900 // 2), 1300, 710, server_list)

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
    clock.tick(120)