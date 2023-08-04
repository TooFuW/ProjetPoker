#Menu du jeu Poker


import pygame
import sys
import webbrowser


class Button:
    """Classe Button pour créer des boutons dynamiques (https://www.youtube.com/watch?v=8SzTzvrWaAA)
    """

    def __init__(self, fonction : str, text : str, police : str, textsize : int, top_color : str, bottom_color : str, width : int, height : int, pos : tuple, elevation : int, round_border : int, image : str = None):
        """Initialisation de la classe Button

        Args:
            fonction (str) : Usage de la fonction, à utiliser dans self.check_click pour lier des actions au bouton correspondant
            text (str): Texte d'affichage du bouton
            police (str): Police d'affichage du texte (seulement parmis les polices système disponibles)
            textsize (int): Taille du texte
            top_color (str): Couleur de la partie haute du bouton (en hexadécimal)
            bottom_color (str): Couleur de la partie basse du bouton (en hexadécimal)
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
        self.pos_x = width_scale(pos[0])
        self.pos_y = height_scale(pos[1])
        self.pos = (self.pos_x, self.pos_y)

        # self.elevation sert à garder la valeur par défaut de l'élévation, on va plutôt utiliser self.dynamic_elevation dans le code
        self.elevation = elevation
        self.dynamic_elevation = elevation
        # On garde la valeur y de pos pour que le mouvement du bouton reste aligné
        self.original_y_pos = self.pos_y

        # Top rectangle
        self.top_rect = pygame.Rect(self.pos, (width_scale(width), height_scale(height)))
        self.top_color = top_color

        # Bottom rectangle
        self.bottom_rect = pygame.Rect(self.pos, (width_scale(width), height_scale(elevation)))
        self.bottom_color = bottom_color

        # Button text
        self.text = text
        gui_font = pygame.font.SysFont(police, width_scale(textsize), False, False)
        self.text_surf = gui_font.render(text, True, "#FFFFFF")
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

        # Button image
        self.image = None
        if image != None:
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, (width_scale(width), height_scale(height)))

    def draw(self):
        """Génération/affichage du bouton
        """
        # Elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        # Affichage de "l'ombre" du bouton qui est sur le "sol"
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius = self.courbure)
        # Affichage du bouton à cliquer
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius = self.courbure)
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
                        game_state.back_pile.append(game_state.state)
                        game_state.state = "Lobby Menu"
                    elif self.fonction == "settings":
                        game_state.back_pile.append(game_state.state)
                        game_state.state = "Setting Menu"
                        game_state.setting_page = 1
                    elif self.fonction == "account":
                        game_state.back_pile.append(game_state.state)
                        game_state.state = "Account Menu"
                    elif self.fonction == "exit":
                        pygame.quit()
                        sys.exit()
                    elif self.fonction == "back":
                        if game_state.back_pile[-1] == "Setting Menu":
                            game_state.setting_page = 1
                        game_state.state = game_state.back_pile.pop()
                    elif self.fonction == "history":
                        game_state.back_pile.append(game_state.state)
                        game_state.state = "History Menu"
                    elif self.fonction == "setting page 1":
                        game_state.setting_page = 1
                    elif self.fonction == "setting page 2":
                        game_state.setting_page = 2
                    elif self.fonction == "setting page 3":
                        game_state.setting_page = 3
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
        self.x = width_scale(x)
        self.default_x = x
        self.y = height_scale(y)
        self.default_y = y
        self.width = width_scale(width)
        self.default_width = width
        self.height = height_scale(height)
        self.servers = servers
        self.scroll_pos = 0
        self.indentation = "          "# Len = 10
        self.hauteurbox = height_scale(50)
        self.selected = False

    def draw(self):
        """Génération/affichage de la scrollbox
        """
        # Créez une surface transparente
        transparent_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Dessinez le rectangle transparent sur la surface
        pygame.draw.rect(transparent_surface, (0, 0, 0, 128), (0, 0, self.width, self.height))
        
        # Afficher la surface transparente sur l'écran
        screen.blit(transparent_surface, (self.x, self.y))

        # Calcul de la zone d'affichage des éléments
        display_area = pygame.Rect(self.x, self.y, self.width, self.height)

        # Décalage initial
        item_offset_y = 0

        # Dessin des éléments visibles
        for i, server in enumerate(self.servers[self.scroll_pos:]):
            item_y = self.default_y + item_offset_y
            # Délimitation de la zone de la scrollbox
            text = (server[0] + self.indentation + str(server[1]) + self.indentation + server[2] + self.indentation + server[3] + self.indentation + server[4] + self.indentation + server[5])
            item_rect = Button("server", text, "Roboto", 24, "#475F77", "#354B5E", self.default_width, self.hauteurbox, (self.default_x, item_y), 3, 0)
            item_rect.check_click()
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if item_rect.top_rect.collidepoint(mouse_pos):
                    self.selected = True
                else:
                    if self.selected == True:
                        # CODE POUR QUAND LES BOUTONS DE SERVEURS SONT CLIQUES /!\ NE PAS LES METTRE DANS LA CLASSE BUTTON CA NE FONCTIONNE PAS /!\
                        game_state.back_pile = ["Main Menu"]
                        game_state.state = "Game Menu"
                        self.selected = False
            else:
                self.selected = False
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
        if self.scroll_pos < width_scale((len(self.servers) - 1) - (self.height // (self.hauteurbox + 10))):
            self.scroll_pos += 1


class TextInputBox:
    """Classe TextInputBox pour gérer des input de texte (https://www.youtube.com/watch?v=Rvcyf4HsWiw&t=323s)
    """

    def __init__(self, text_size : int, pos : tuple, width : int, height : int, active_color : str, passive_color : str, base_size : int, adaptative : bool = True, max_caracteres : int = -1, num_only : bool = False):
        """Initialisation des paramètres des TextInputBox

        Args:
            text_size (int): Taille du texte
            pos (tuple): Position x, y de la boîte
            width (int): Largeur de la boîte
            height (int): Hauteur de la boîte
            active_color (str): Couleur de la boîte lorsque l'on peut écrire dedans
            passive_color (str): Couleur de la boîte lorsque l'on ne peut pas écrire dedans
            base_size (int): Taille minimum de la box (DOIT ETRE EGAL A WIDTH SI ADAPTATIVE = FALSE)
            adaptative (bool) = True: True si la taille de la boîte peut changer en fonction de la taille du texte, False si elle est fixe (le texte ne pourra alors pas dépasser de la boîte)
            max_caractere (int) = -1: -1 si les caractères sont illimités, entier positif sinon
            num_only (bool) = False: True si on ne peut entrer que des chiffres, False sinon
        """
        # Paramères du texte
        self.base_font = pygame.font.SysFont("Roboto", width_scale(text_size))
        self.user_text = ""
        self.max_caracteres = max_caracteres
        # Position du texte
        self.input_rect = pygame.Rect(width_scale(pos[0]), height_scale(pos[1]), width_scale(width), height_scale(height))
        # Couleur de la box en fonction si elle est sélecionnée ou non
        self.color_active = active_color
        self.color_passive = passive_color
        self.color = self.color_passive
        self.active = False
        self.base_size = base_size
        self.adaptative_size = adaptative
        self.text_size = 0
        self.num_only = num_only
    
    def draw(self):
        """On dessine la box et le texte écrit par l'utilisateur
        """
        # On récupére la position de la souris
        mouse_pos = pygame.mouse.get_pos()
        # On vérifie si la box a été sélectionnée
        if pygame.mouse.get_pressed()[0]:
            if self.input_rect.collidepoint(mouse_pos):
                self.active = True
            else:
                self.active = False
        # On définit la couleur de la box en fonction de si elle est sélectionnée ou non
        if self.active == True:
                self.color = self.color_active
        else:
            self.color = self.color_passive
        # On dessine le texte et la box
        pygame.draw.rect(screen, self.color, self.input_rect, border_radius = 10)
        text_surface = self.base_font.render(self.user_text, True, "#FFFFFF")
        self.text_size = text_surface.get_width() + 25
        screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        # On crée une taille de box adaptative
        if self.adaptative_size == True:
            # Taille de la box qui est de base 200 et qui augmente si le texte dépasse
            self.input_rect.w = width_scale(max(self.base_size, text_surface.get_width() + 10))
        else:
            self.input_rect.w = width_scale(self.base_size)


class Preview_Table:
    """Classe Preview_Table pour afficher des previews de tables
    """

    def __init__(self, pos : tuple, scale : float = 1):
        """Initialisation des paramètres des previews

        Args:
            pos (tuple): Position x, y de la preview
            scale (float) = 1: Multiplicateur de taille de la preview (1 par défaut)
        """
        self.x = width_scale(pos[0])
        self.y = height_scale(pos[1])
        self.width = width_scale(500*scale)
        self.height = height_scale(500*scale)

    def draw(self):
        """Génération/affichage de la preview
        """
        
        # Dessinez la zone de la preview sur l'écran
        pygame.draw.rect(screen, "#006400", (self.x, self.y, self.width, self.height), border_radius = 10)



class HUD_State:
    """Classe HUD_State pour gérer l'interface active (https://www.youtube.com/watch?v=j9yMFG3D7fg)
    """

    def __init__(self):
        """Initialisation de l'état de l'interface
        """
        # self.state définit l'état actuel de l'interface (qui est par défaut Main Menu)
        self.state = "Main Menu"
        self.back_pile = []
        self.is_pressing_logomwte = False
        self.setting_page = 1
    
    def mainmenu(self):
        """mainmenu est la fonction qui fait tourner/afficher le menu principal
        """
        # Rassemblement de tout les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Dessine l'image de fond sur le screen de l'écran
        screen.blit(fond, (0, 0))
        # Dessine le logo du jeu
        screen.blit(logojeu, (width_scale(800), height_scale(40)))
        # Dessine le logo MWTE
        screen.blit(logomwte, logomwte_rect)

        # Lien associé au logo MWTE
        # On récupére la position de la souris
        mouse_pos = pygame.mouse.get_pos()
        # On vérifie si la position de la souris est sur le bouton
        if logomwte_rect.collidepoint(mouse_pos):
            gui_font = pygame.font.SysFont("Roboto", 20, False, True)
            text_surf = gui_font.render("Aller sur le site officiel MWTE", True, "#000000")
            pygame.draw.rect(screen, "#FFFFFF", pygame.Rect((mouse_pos[0], mouse_pos[1] + 15), (200, 20)), border_radius = 3)
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
        # Affichage des chips de l'utilisateur à droite du bouton ACCOUNT
        gui_font = pygame.font.SysFont("Roboto", 40)
        text_surf = gui_font.render("Chips : ", True, "#FFFFFF")
        pygame.draw.rect(screen, "#475F77", pygame.Rect((width_scale(1540), height_scale(30)), (width_scale(200), height_scale(50))), border_radius = 3)
        screen.blit(text_surf, (width_scale(1550), height_scale(40)))
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
            # Si on a sélectionne la TextInputBox
            if tablecodeinput.active == True:
                if event.type == pygame.KEYDOWN:
                    # Si on clique sur delete
                    if event.key == pygame.K_BACKSPACE:
                        tablecodeinput.user_text = tablecodeinput.user_text[:-1]
                    # Si on clique sur entrer
                    elif event.key == pygame.K_RETURN:
                        tablecodeinput.user_text = ""
                    # Si on clique sur n'importe quoi d'autre
                    else:
                        if tablecodeinput.num_only == True:
                            if event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                if tablecodeinput.max_caracteres > 0:
                                    if len(tablecodeinput.user_text) < tablecodeinput.max_caracteres:
                                        if tablecodeinput.adaptative_size == False:
                                            if tablecodeinput.text_size < tablecodeinput.base_size:
                                                tablecodeinput.user_text += event.unicode
                                        else:
                                            tablecodeinput.user_text += event.unicode
                        else:
                            if tablecodeinput.max_caracteres > 0:
                                if len(tablecodeinput.user_text) < tablecodeinput.max_caracteres:
                                    if tablecodeinput.adaptative_size == False:
                                        if tablecodeinput.text_size < tablecodeinput.base_size:
                                            tablecodeinput.user_text += event.unicode
                                        else:
                                            tablecodeinput.user_text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Molette de la souris vers le haut
                if event.button == 4:
                    serverscrollbox.scroll_up()
                # Molette de la souris vers le bas    
                elif event.button == 5:
                    serverscrollbox.scroll_down()

        # Dessine l'image de fond sur la screen de l'écran
        screen.blit(fond, (0, 0))

        # Dessin de la scrollbox
        serverscrollbox.draw()

        # Affichage des bouttons
        # Cliquer sur le bouton BACK ferme la fenêtre purement et simplement
        backbutton.draw()
        # Cliquer sur le bouton CREER TABLE crée une nouvelle table
        createtablebutton.draw()
        # Cliquer sur le bouton ACCOUNT ouvre l'interface présentant les informations du compte actif
        accountbutton.draw()
        # Affichage des chips de l'utilisateur à droite du bouton ACCOUNT
        gui_font = pygame.font.SysFont("Roboto", 40)
        text_surf = gui_font.render("Chips : ", True, "#FFFFFF")
        pygame.draw.rect(screen, "#475F77", pygame.Rect((width_scale(1540), height_scale(30)), (width_scale(200), height_scale(50))), border_radius = 3)
        screen.blit(text_surf, (width_scale(1550), height_scale(40)))

        # On crée la box dans laquelle on pourra écrire un code de partie pour rejoindre
        tablecodeinput.draw()
        # On affiche un texte au-dessus de la box qui indique ce que cette dernière fait
        gui_font = pygame.font.SysFont("Roboto", 50)
        text_surf = gui_font.render("Private Table Code", True, "#000000")
        text_rect = text_surf.get_rect(center = pygame.Rect((width_scale(1445), height_scale(735)), (width_scale(150), height_scale(75))).center)
        screen.blit(text_surf, text_rect)

        # On crée la preview des tables
        previewlobbys.draw()
        
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

        # Affichage des bouttons
        # Cliquer sur le bouton BACK ferme la fenêtre purement et simplement
        backbutton.draw()
        # Cliquer sur le bouton ACCOUNT ouvre l'interface présentant les informations du compte actif
        accountbutton.draw()
        # Affichage des chips de l'utilisateur à droite du bouton ACCOUNT
        gui_font = pygame.font.SysFont("Roboto", 40)
        text_surf = gui_font.render("Chips : ", True, "#FFFFFF")
        pygame.draw.rect(screen, "#475F77", pygame.Rect((width_scale(1540), height_scale(30)), (width_scale(200), height_scale(50))), border_radius = 3)
        screen.blit(text_surf, (width_scale(1550), height_scale(40)))

        # Affichage des boutons de pages de paramètres
        settingpage1button.draw()
        settingpage2button.draw()
        settingpage3button.draw()
        # Affichage des pages de paramètres
        transparent_surface = pygame.Surface((width_scale(1500), height_scale(850)), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 128), (0, 0, 1500, 850), border_radius = 5)
        screen.blit(transparent_surface, (width_scale(260), height_scale(160)))
        screen.blit(transparent_surface, (width_scale(260), height_scale(160)))
        screen.blit(transparent_surface, (width_scale(260), height_scale(160)))
        # Page 1
        if self.setting_page == 1:
            gui_font = pygame.font.SysFont("Roboto", 40)
            settingtext_surf = gui_font.render("Page 1 des paramètres", True, "#FFFFFF")
            screen.blit(settingtext_surf, (width_scale(270), height_scale(170)))
        # Page 2
        elif self.setting_page == 2:
            gui_font = pygame.font.SysFont("Roboto", 40)
            settingtext_surf = gui_font.render("Page 2 des paramètres", True, "#FFFFFF")
            screen.blit(settingtext_surf, (width_scale(270), height_scale(170)))
        # Page 3
        elif self.setting_page == 3:
            gui_font = pygame.font.SysFont("Roboto", 40)
            settingtext_surf = gui_font.render("Page 3 des paramètres", True, "#FFFFFF")
            screen.blit(settingtext_surf, (width_scale(270), height_scale(170)))

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

        # Affichage des bouttons
        # Cliquer sur le bouton BACK ferme la fenêtre purement et simplement
        backbutton.draw()

        # Dessin des infos du compte
        # Affichage de la pdp de l'utilisateur
        screen.blit(pdpplayer, (width_scale(360), height_scale(190)))
        # Affichage des chips de l'utilisateur
        gui_font = pygame.font.SysFont("Roboto", 40)
        text_surf = gui_font.render("Chips : ", True, "#FFFFFF")
        pygame.draw.rect(screen, "#475F77", pygame.Rect((width_scale(400), height_scale(465)), (width_scale(225), height_scale(50))), border_radius = 3)
        screen.blit(text_surf, (width_scale(410), height_scale(475)))
        # Affichage du pseudo de l'utilisateur
        gui_font = pygame.font.SysFont("Roboto", 60)
        text_surf = gui_font.render("PSEUDO", True, "#FFFFFF")
        pygame.draw.rect(screen, "#475F77", pygame.Rect((width_scale(685), height_scale(190)), (width_scale(600), height_scale(100))), border_radius = 3)
        screen.blit(text_surf, (width_scale(695), height_scale(220)))
        # Affichage des infos de l'utilisateur
        gui_font = pygame.font.SysFont("Roboto", 60)
        text_surf = gui_font.render("INFORMATIONS", True, "#FFFFFF")
        pygame.draw.rect(screen, "#475F77", pygame.Rect((width_scale(685), height_scale(315)), (width_scale(600), height_scale(650))), border_radius = 3)
        screen.blit(text_surf, (width_scale(695), height_scale(325)))
        # Affichage du bouton de déconnexion de l'utilisateur
        deconnexionbutton.draw()
        # Affichage du bouton de paramètres du compte de l'utilisateur
        accountsettingsbutton.draw()
        
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Molette de la souris vers le haut
                if event.button == 4:
                    historyscrollbox.scroll_up()
                # Molette de la souris vers le bas    
                elif event.button == 5:
                    historyscrollbox.scroll_down()

        # Dessine l'image de fond sur la screen de l'écran (IMPORANT CAR SE SUPERPOSE A L'INTERFACE PRECEDENT ET PERMET DE "L'EFFACER")
        screen.blit(fond, (0, 0))

        # Dessin de la scrollbox
        historyscrollbox.draw()  

        # On crée la preview des tables
        previewhistory.draw()

        # Affichage des bouttons
        # Cliquer sur le bouton BACK ferme la fenêtre purement et simplement
        backbutton.draw()
        # Cliquer sur le bouton ACCOUNT ouvre l'interface présentant les informations du compte actif
        accountbutton.draw()
        # Affichage des chips de l'utilisateur à droite du bouton ACCOUNT
        gui_font = pygame.font.SysFont("Roboto", 40)
        text_surf = gui_font.render("Chips : ", True, "#FFFFFF")
        pygame.draw.rect(screen, "#475F77", pygame.Rect((width_scale(1540), height_scale(30)), (width_scale(200), height_scale(50))), border_radius = 3)
        screen.blit(text_surf, (width_scale(1550), height_scale(40)))

        # Met à jour l'affichage de l'interface
        pygame.display.update()

    def gamemenu(self):
        """historymenu est la fonction qui fait tourner/afficher le menu de l'historique des parties du compte actif
        """
        # Rassemblement de tout les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Dessine l'image de fond sur la screen de l'écran (IMPORANT CAR SE SUPERPOSE A L'INTERFACE PRECEDENT ET PERMET DE "L'EFFACER")
        screen.blit(fond, (0, 0))

        # Affichage des bouttons
        # Cliquer sur le bouton BACK ferme la fenêtre purement et simplement
        backbutton.draw()
        # Cliquer sur le bouton ACCOUNT ouvre l'interface présentant les informations du compte actif
        accountbutton.draw()
        # Affichage des chips de l'utilisateur à droite du bouton ACCOUNT
        gui_font = pygame.font.SysFont("Roboto", 40)
        text_surf = gui_font.render("Chips : ", True, "#FFFFFF")
        pygame.draw.rect(screen, "#475F77", pygame.Rect((width_scale(1540), height_scale(30)), (width_scale(200), height_scale(50))), border_radius = 3)
        screen.blit(text_surf, (width_scale(1550), height_scale(40)))

        # Met à jour l'affichage de l'interface
        pygame.display.update()
    
    def state_manager(self):
        """state_manager se charge d'afficher la bonne interface en fonction de l'état de self.state
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
        elif self.state == "Game Menu":
            self.gamemenu()


def width_scale(largeur : int):
    """Fonction qui permet de donner une largeur adaptée à la largeur de l'écran (par rapport à un écran de 17 pouces/1920px)

    Args:
        largeur (int): largeur à transformer

    Returns:
        width (int): largeur adaptée
    """
    width = largeur*largeur_actuelle//1920
    return width

def height_scale(hauteur : int):
    """Fonction qui permet de donner une hauteur adaptée à la hauteur de l'écran (par rapport à un écran de 17 pouces/1080px)

    Args:
        hauteur (int): hauteur à transformer

    Returns:
        height (int): hauteur adaptée
    """
    height = hauteur*hauteur_actuelle//1080
    return height


# Pygame setup
pygame.init()
game_state = HUD_State()
# Taille de la fenêtre
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
largeur_actuelle = screen.get_width()
hauteur_actuelle = screen.get_height()
# Nom de la fenêtre
pygame.display.set_caption("Menu Jeu Poker")
clock = pygame.time.Clock()

# Récupération de la liste des lobbys disponibles et de leurs informations ([0] = Nom de la table, [1] = Nombre de joueurs/nombre de joueurs max, [2] = Montant de la mise, [3] = Pot moyen, [4] = Tapis moyen, [5] = ID de la table)
server_list = [["Table 1", "0/5", "50/100", "15K", "25K", "ID1"], ["Table 2", "1/6", "50/100", "10K", "20K", "ID2"], ["Table 3", "2/7", "50/100", "20K", "30K", "ID3"], ["Table 4", "3/8", "50/100", "5K", "15K", "ID4"], ["Table 5", "4/9", "50/100", "8K", "18K", "ID5"], ["Table 6", "5/9", "50/100", "8K", "18K", "ID6"], ["Table 7", "6/9", "50/100", "11K", "21K", "ID7"], ["Table 8", "7/9", "50/100", "18K", "28K", "ID8"], ["Table 9", "8/9", "50/100", "12K", "22K", "ID9"], ["Table 10", "9/9", "50/100", "3K", "13K", "ID10"], ["Table 11", "0/6", "50/100", "15K", "25K", "ID11"], ["Table 12", "1/7", "50/100", "10K", "20K", "ID12"], ["Table 13", "2/8", "50/100", "20K", "30K", "ID13"], ["Table 14", "3/9", "50/100", "5K", "15K", "ID14"], ["Table 15", "4/9", "50/100", "8K", "18K", "ID15"], ["Table 16", "5/9", "50/100", "8K", "18K", "ID16"], ["Table 17", "6/9", "50/100", "11K", "21K", "ID17"], ["Table 18", "7/9", "50/100", "18K", "28K", "ID18"], ["Table 19", "8/9", "50/100", "12K", "22K", "ID19"], ["Table 20", "9/9", "50/100", "3K", "13K", "ID20"]]

# Chargement de l'image de fond
pokertablebackground = pygame.image.load("PokerBackground.jpg")
fond = pygame.transform.scale(pokertablebackground, (screen_width, screen_height))

# Chargement du logo du jeu
logojeu = pygame.image.load("PokerBackground.jpg")
logojeu = pygame.transform.scale(logojeu, (width_scale(250), height_scale(250)))

# Chargement du logo MWTE
logomwte = pygame.image.load("logo mwte.jpg")
logomwte = pygame.transform.scale(logomwte, (width_scale(175), height_scale(175)))
logomwte_rect = logomwte.get_rect()
logomwte_rect.topleft = (width_scale(10), height_scale(890))

# Chargement de la photo de profil du joueur
pdpplayer = pygame.image.load("logo mwte.jpg")
pdpplayer = pygame.transform.scale(pdpplayer, (width_scale(300), height_scale(300)))

# Création de tout les boutons utilisés
# Création de l'objet accountbutton
accountbutton = Button("account", "ACCOUNT", "Roboto", 30, "#475F77", "#354B5E", 150, 75, (1750, 20), 3, 10)
# Création de l'objet playbutton
playbutton = Button("play", "PLAY", "Roboto", 150, "#475F77", "#354B5E", 500, 500, (710, 365), 6, 10)
# Création de l'objet settingsbutton
settingsbutton = Button("settings", "SETTINGS", "Roboto", 70, "#475F77", "#354B5E", 300, 500, (310, 365), 6, 10)
# Création de l'objet quitbutton
exitbutton = Button("exit", "EXIT", "Roboto", 70, "#475F77", "#354B5E", 400, 100, (760, 960), 6, 10)
# Création de l'objet backbutton
backbutton = Button("back", "", "Roboto", 0, "#475F77", "#354B5E", 125, 125, (25, 25), 6, 10, "backarrow.png")
# Création de l'objet createtablebutton
createtablebutton = Button("create table", "CREATE TABLE", "Roboto", 60, "#475F77", "#354B5E", 400, 100, (175, 50), 6, 10)
# Création de l'objet gamehistorybutton
gamehistorybutton = Button("history", "HISTORY", "Roboto", 70, "#475F77", "#354B5E", 300, 500, (1310, 365), 6, 10)
# Création de l'objet deconnexionbutton
deconnexionbutton = Button("deconnexion", "LOG OUT", "Roboto", 60, "#475F77", "#354B5E", 300, 100, (1605, 970), 6, 10)
# Création de l'objet accountsettingsbutton
accountsettingsbutton = Button("account settings", "", "Roboto", 0, "#475F77", "#354B5E", 125, 125, (1770, 25), 6, 10,"settinglogo.png")
# Création de l'objet settingpage1button
settingpage1button = Button("setting page 1", "PAGE 1", "Roboto", 50, "#475F77", "#354B5E", 200, 70, (260, 90), 4, 8)
# Création de l'objet settingpage1button
settingpage2button = Button("setting page 2", "PAGE 2", "Roboto", 50, "#475F77", "#354B5E", 200, 70, (470, 90), 4, 8)
# Création de l'objet settingpage1button
settingpage3button = Button("setting page 3", "PAGE 3", "Roboto", 50, "#475F77", "#354B5E", 200, 70, (680, 90), 4, 8)

# Création des scrollboxs
# Création de l'objet serverscrollbox 
serverscrollbox = ScrollBox(210, 215, 1000, 760, server_list)
# Création de l'objet historyscrollbox
historyscrollbox = ScrollBox(210, 215, 1000, 760, server_list)

#Création de l'objet tablecodeinput
tablecodeinput = TextInputBox(150, (1360, 790), 400, 100, "#333333", "#888888", 400, False, 6, True)

# Création des previews de tables
# Création de l'objet previewlobbys
previewlobbys = Preview_Table((1310, 215))
# Création de l'objet previewhistory
previewhistory = Preview_Table((1310, 215))

# Gameloop
while True:
    largeur_actuelle = screen.get_width()
    hauteur_actuelle = screen.get_height()
    # Chargement de la musique de fond et mise en boucle
    if pygame.mixer.music.get_busy() != True:
        pygame.mixer.music.load("mainmenu_soundtrack.mp3")
        pygame.mixer.music.rewind()
        pygame.mixer.music.play()
    # Cet appel permet de gérer l'interface active
    game_state.state_manager()
    # Limite les FPS à 60
    clock.tick(120)