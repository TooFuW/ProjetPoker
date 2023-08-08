#Menu du jeu Poker


import pygame
import webbrowser
from Screen_adaptation import *
from Button_class import *
import Global_objects


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
        self.x = width_scale(x, largeur_actuelle)
        self.default_x = x
        self.y = height_scale(y, hauteur_actuelle)
        self.default_y = y
        self.width = width_scale(width, largeur_actuelle)
        self.default_width = width
        self.height = height_scale(height, hauteur_actuelle)
        self.servers = servers
        self.scroll_pos = 0
        self.indentation = "          "# Len = 10
        self.hauteurbox = height_scale(50, hauteur_actuelle)
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
            item_rect = Button(largeur_actuelle, hauteur_actuelle, screen, "server", text, "Roboto", 24, "#475F77", "#354B5E", "#D74B4B", self.default_width, self.hauteurbox, (self.default_x, item_y), 3, 0)
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
        if self.scroll_pos < width_scale((len(self.servers) - 1) - (self.height // (self.hauteurbox + 10)), largeur_actuelle):
            self.scroll_pos += 1


class TextInputBox:
    """Classe TextInputBox pour gérer des input de texte (https://www.youtube.com/watch?v=Rvcyf4HsWiw&t=323s)
    """

    def __init__(self, text_size : int, pos : tuple, width : int, height : int, active_color : str, passive_color : str, base_size : int, adaptative : bool = True, max_caracteres : int = -1, num_only : bool = False, interactible : bool = True, starting_text : str = ""):
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
            interactible (bool) = True: True si on peut interagir avec, False sinon
            starting_text (str) = "": Chaîne de caractère vide par défaut, sinon le texte de départ
        """
        # Paramères du texte
        self.base_font = pygame.font.SysFont("Roboto", width_scale(text_size, largeur_actuelle))
        self.user_text = starting_text
        self.max_caracteres = max_caracteres
        # Position du texte
        self.input_rect = pygame.Rect(width_scale(pos[0], largeur_actuelle), height_scale(pos[1], hauteur_actuelle), width_scale(width, largeur_actuelle), height_scale(height, hauteur_actuelle))
        # Couleur de la box en fonction si elle est sélecionnée ou non
        self.color_active = active_color
        self.color_passive = passive_color
        self.color = self.color_passive
        self.active = False
        self.base_size = base_size
        self.adaptative_size = adaptative
        self.text_size = 0
        self.num_only = num_only
        self.interactible = interactible
    
    def draw(self):
        """On dessine la box et le texte écrit par l'utilisateur
        """
        # On récupére la position de la souris
        mouse_pos = pygame.mouse.get_pos()
        # On vérifie si la box a été sélectionnée
        if pygame.mouse.get_pressed()[0]:
            if self.interactible == True:
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
        # Dessin du texte par lignes si la box n'est pas adaptative et que le texte dépasse, sinon le texte est dessiné normalement
        if self.adaptative_size == False:
            y = self.input_rect.y + 5
            for line in self.user_text.split("\n"):
                text_surface = self.base_font.render(line, True, "#FFFFFF")
                screen.blit(text_surface, (self.input_rect.x + 5, y))
                y += text_surface.get_height()
        else:
            text_surface = self.base_font.render(self.user_text, True, "#FFFFFF")
            screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.text_size = text_surface.get_width() + 25
        # On crée une taille de box adaptative
        if self.adaptative_size == True:
            # Taille de la box qui est de base 200 et qui augmente si le texte dépasse
            self.input_rect.w = width_scale(max(self.base_size, text_surface.get_width() + 10), largeur_actuelle)
        else:
            self.input_rect.w = width_scale(self.base_size, largeur_actuelle)
            # Si le texte dépasse mais que la box n'est pas adaptative on retourne à la ligne
            if text_surface.get_width() + 20 > self.base_size:
                self.user_text += "\n"


class Preview_Table:
    """Classe Preview_Table pour afficher des previews de tables
    """

    def __init__(self, pos : tuple, scale : float = 1):
        """Initialisation des paramètres des previews

        Args:
            pos (tuple): Position x, y de la preview
            scale (float) = 1: Multiplicateur de taille de la preview (1 par défaut)
        """
        self.x = width_scale(pos[0], largeur_actuelle)
        self.y = height_scale(pos[1], hauteur_actuelle)
        self.width = width_scale(500*scale, largeur_actuelle)
        self.height = height_scale(500*scale, hauteur_actuelle)

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
        screen.blit(logojeu, (width_scale(800, largeur_actuelle), height_scale(40, hauteur_actuelle)))
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
        pygame.draw.rect(screen, "#475F77", pygame.Rect((width_scale(1540, largeur_actuelle), height_scale(30, hauteur_actuelle)), (width_scale(200, largeur_actuelle), height_scale(50, hauteur_actuelle))), border_radius = 3)
        screen.blit(text_surf, (width_scale(1550, largeur_actuelle), height_scale(40, hauteur_actuelle)))
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
        pygame.draw.rect(screen, "#475F77", pygame.Rect((width_scale(1540, largeur_actuelle), height_scale(30, hauteur_actuelle)), (width_scale(200, largeur_actuelle), height_scale(50, hauteur_actuelle))), border_radius = 3)
        screen.blit(text_surf, (width_scale(1550, largeur_actuelle), height_scale(40, hauteur_actuelle)))

        # On crée la box dans laquelle on pourra écrire un code de partie pour rejoindre
        tablecodeinput.draw()
        # On affiche un texte au-dessus de la box qui indique ce que cette dernière fait
        gui_font = pygame.font.SysFont("Roboto", 50)
        text_surf = gui_font.render("Private Table Code", True, "#000000")
        text_rect = text_surf.get_rect(center = pygame.Rect((width_scale(1445, largeur_actuelle), height_scale(735, hauteur_actuelle)), (width_scale(150, largeur_actuelle), height_scale(75, hauteur_actuelle))).center)
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
        pygame.draw.rect(screen, "#475F77", pygame.Rect((width_scale(1540, largeur_actuelle), height_scale(30, hauteur_actuelle)), (width_scale(200, largeur_actuelle), height_scale(50, hauteur_actuelle))), border_radius = 3)
        screen.blit(text_surf, (width_scale(1550, largeur_actuelle), height_scale(40, hauteur_actuelle)))

        # Affichage des boutons de pages de paramètres
        settingpage1button.draw()
        settingpage2button.draw()
        settingpage3button.draw()
        # Affichage des pages de paramètres
        transparent_surface = pygame.Surface((width_scale(1500, largeur_actuelle), height_scale(850, hauteur_actuelle)), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 128), (0, 0, 1500, 850), border_radius = 5)
        screen.blit(transparent_surface, (width_scale(260, largeur_actuelle), height_scale(160, hauteur_actuelle)))
        screen.blit(transparent_surface, (width_scale(260, largeur_actuelle), height_scale(160, hauteur_actuelle)))
        screen.blit(transparent_surface, (width_scale(260, largeur_actuelle), height_scale(160, hauteur_actuelle)))
        # Page 1
        if self.setting_page == 1:
            gui_font = pygame.font.SysFont("Roboto", 40)
            settingtext_surf = gui_font.render("Page 1 des paramètres", True, "#FFFFFF")
            screen.blit(settingtext_surf, (width_scale(270, largeur_actuelle), height_scale(170, hauteur_actuelle)))
        # Page 2
        elif self.setting_page == 2:
            gui_font = pygame.font.SysFont("Roboto", 40)
            settingtext_surf = gui_font.render("Page 2 des paramètres", True, "#FFFFFF")
            screen.blit(settingtext_surf, (width_scale(270, largeur_actuelle), height_scale(170, hauteur_actuelle)))
        # Page 3
        elif self.setting_page == 3:
            gui_font = pygame.font.SysFont("Roboto", 40)
            settingtext_surf = gui_font.render("Page 3 des paramètres", True, "#FFFFFF")
            screen.blit(settingtext_surf, (width_scale(270, largeur_actuelle), height_scale(170, hauteur_actuelle)))

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
            # Si on a sélectionne la accountpseudoinput
            if accountpseudoinput.active == True:
                if event.type == pygame.KEYDOWN:
                    # Si on clique sur delete
                    if event.key == pygame.K_BACKSPACE:
                        accountpseudoinput.user_text = accountpseudoinput.user_text[:-1]
                    # Si on clique sur entrer
                    elif event.key == pygame.K_RETURN:
                        accountpseudoinput.user_text = ""
                    # Si on clique sur n'importe quoi d'autre
                    else:
                        if accountpseudoinput.num_only == True:
                            if event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                if accountpseudoinput.max_caracteres > 0:
                                    if len(accountpseudoinput.user_text) < accountpseudoinput.max_caracteres:
                                        if accountpseudoinput.adaptative_size == False:
                                            if accountpseudoinput.text_size < accountpseudoinput.base_size:
                                                accountpseudoinput.user_text += event.unicode
                                        else:
                                            accountpseudoinput.user_text += event.unicode
                        else:
                            if accountpseudoinput.max_caracteres > 0:
                                if len(accountpseudoinput.user_text) < accountpseudoinput.max_caracteres:
                                    if accountpseudoinput.adaptative_size == False:
                                        if accountpseudoinput.text_size < accountpseudoinput.base_size:
                                            accountpseudoinput.user_text += event.unicode
                                        else:
                                            accountpseudoinput.user_text += event.unicode
                                    else:
                                        accountpseudoinput.user_text += event.unicode
            # Si on a sélectionne la accountpseudoinput
            if accountinformationinput.active == True:
                if event.type == pygame.KEYDOWN:
                    # Si on clique sur delete
                    if event.key == pygame.K_BACKSPACE:
                        accountinformationinput.user_text = accountinformationinput.user_text[:-1]
                    # Si on clique sur entrer
                    elif event.key == pygame.K_RETURN:
                        accountinformationinput.user_text = ""
                    # Si on clique sur n'importe quoi d'autre
                    else:
                        if accountinformationinput.num_only == True:
                            if event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                if accountinformationinput.max_caracteres > 0:
                                    if len(accountinformationinput.user_text) < accountinformationinput.max_caracteres:
                                        if accountinformationinput.adaptative_size == False:
                                            if accountinformationinput.text_size < accountinformationinput.base_size:
                                                accountinformationinput.user_text += event.unicode
                                        else:
                                            accountinformationinput.user_text += event.unicode
                        else:
                            if accountinformationinput.max_caracteres > 0:
                                if len(accountinformationinput.user_text) < accountinformationinput.max_caracteres:
                                    if accountinformationinput.adaptative_size == False:
                                        if accountinformationinput.text_size < accountinformationinput.base_size:
                                            accountinformationinput.user_text += event.unicode
                                        else:
                                            accountinformationinput.user_text += event.unicode
                                    else:
                                        accountinformationinput.user_text += event.unicode


        # Dessine l'image de fond sur la screen de l'écran (IMPORANT CAR SE SUPERPOSE A L'INTERFACE PRECEDENT ET PERMET DE "L'EFFACER")
        screen.blit(fond, (0, 0))

        # Affichage des bouttons
        # Cliquer sur le bouton BACK ferme la fenêtre purement et simplement
        backbutton.draw()

        # Dessin des infos du compte
        # Affichage de la pdp de l'utilisateur
        screen.blit(pdpplayer, (width_scale(360, largeur_actuelle), height_scale(190, hauteur_actuelle)))
        # Affichage des chips de l'utilisateur
        gui_font = pygame.font.SysFont("Roboto", 40)
        text_surf = gui_font.render("Chips : ", True, "#FFFFFF")
        pygame.draw.rect(screen, "#475F77", pygame.Rect((width_scale(400, largeur_actuelle), height_scale(465, hauteur_actuelle)), (width_scale(225, largeur_actuelle), height_scale(50, hauteur_actuelle))), border_radius = 3)
        screen.blit(text_surf, (width_scale(410, largeur_actuelle), height_scale(475, hauteur_actuelle)))
        # Affichage du pseudo de l'utilisateur
        accountpseudoinput.draw()
        # Affichage des infos de l'utilisateur
        accountinformationinput.draw()
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
        pygame.draw.rect(screen, "#475F77", pygame.Rect((width_scale(1540, largeur_actuelle), height_scale(30, hauteur_actuelle)), (width_scale(200, largeur_actuelle), height_scale(50, hauteur_actuelle))), border_radius = 3)
        screen.blit(text_surf, (width_scale(1550, largeur_actuelle), height_scale(40, hauteur_actuelle)))

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
        accountsettingsbutton.draw()
        # Affichage des chips de l'utilisateur à droite du bouton ACCOUNT
        gui_font = pygame.font.SysFont("Roboto", 40)
        text_surf = gui_font.render("Loading table...", True, "#FFFFFF")
        pygame.draw.rect(screen, "#475F77", pygame.Rect((width_scale(700, largeur_actuelle), height_scale(500, hauteur_actuelle)), (width_scale(250, largeur_actuelle), height_scale(50, hauteur_actuelle))), border_radius = 3)
        screen.blit(text_surf, (width_scale(710, largeur_actuelle), height_scale(510, hauteur_actuelle)))

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


# Pygame setup
pygame.init()
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
# Initialisation de la fenêtre actuelle
game_state = HUD_State()

# Récupération de la liste des lobbys disponibles et de leurs informations ([0] = Nom de la table, [1] = Nombre de joueurs/nombre de joueurs max, [2] = Montant de la mise, [3] = Pot moyen, [4] = Tapis moyen, [5] = ID de la table)
server_list = [["Table 1", "0/5", "50/100", "15K", "25K", "ID1"], ["Table 2", "1/6", "50/100", "10K", "20K", "ID2"], ["Table 3", "2/7", "50/100", "20K", "30K", "ID3"], ["Table 4", "3/8", "50/100", "5K", "15K", "ID4"], ["Table 5", "4/9", "50/100", "8K", "18K", "ID5"], ["Table 6", "5/9", "50/100", "8K", "18K", "ID6"], ["Table 7", "6/9", "50/100", "11K", "21K", "ID7"], ["Table 8", "7/9", "50/100", "18K", "28K", "ID8"], ["Table 9", "8/9", "50/100", "12K", "22K", "ID9"], ["Table 10", "9/9", "50/100", "3K", "13K", "ID10"], ["Table 11", "0/6", "50/100", "15K", "25K", "ID11"], ["Table 12", "1/7", "50/100", "10K", "20K", "ID12"], ["Table 13", "2/8", "50/100", "20K", "30K", "ID13"], ["Table 14", "3/9", "50/100", "5K", "15K", "ID14"], ["Table 15", "4/9", "50/100", "8K", "18K", "ID15"], ["Table 16", "5/9", "50/100", "8K", "18K", "ID16"], ["Table 17", "6/9", "50/100", "11K", "21K", "ID17"], ["Table 18", "7/9", "50/100", "18K", "28K", "ID18"], ["Table 19", "8/9", "50/100", "12K", "22K", "ID19"], ["Table 20", "9/9", "50/100", "3K", "13K", "ID20"]]

# Chargement de l'image de fond
pokertablebackground = pygame.image.load("PokerBackground.jpg")
fond = pygame.transform.scale(pokertablebackground, (screen_width, screen_height))

# Chargement du logo du jeu
logojeu = pygame.image.load("PokerBackground.jpg")
logojeu = pygame.transform.scale(logojeu, (width_scale(250, largeur_actuelle), height_scale(250, hauteur_actuelle)))

# Chargement du logo MWTE
logomwte = pygame.image.load("logo mwte.jpg")
logomwte = pygame.transform.scale(logomwte, (width_scale(175, largeur_actuelle), height_scale(175, hauteur_actuelle)))
logomwte_rect = logomwte.get_rect()
logomwte_rect.topleft = (width_scale(10, largeur_actuelle), height_scale(890, hauteur_actuelle))

# Chargement de la photo de profil du joueur
pdpplayer = pygame.image.load("logo mwte.jpg")
pdpplayer = pygame.transform.scale(pdpplayer, (width_scale(300, largeur_actuelle), height_scale(300, hauteur_actuelle)))

# Création de tout les boutons utilisés
# Création de l'objet accountbutton
accountbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "account", "ACCOUNT", "Roboto", 30, "#475F77", "#354B5E", "#D74B4B", 150, 75, (1750, 20), 3, 10)
# Création de l'objet playbutton
playbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "play", "PLAY", "Roboto", 150, "#475F77", "#354B5E", "#D74B4B", 500, 500, (710, 365), 6, 10)
# Création de l'objet settingsbutton
settingsbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "settings", "SETTINGS", "Roboto", 70, "#475F77", "#354B5E", "#D74B4B", 300, 500, (310, 365), 6, 10)
# Création de l'objet quitbutton
exitbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "exit", "EXIT", "Roboto", 70, "#475F77", "#354B5E", "#D74B4B", 400, 100, (760, 960), 6, 10)
# Création de l'objet backbutton
backbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "back", "", "Roboto", 0, "#475F77", "#354B5E", "#D74B4B", 125, 125, (25, 25), 6, 10, "backarrow.png")
# Création de l'objet createtablebutton
createtablebutton = Button(largeur_actuelle, hauteur_actuelle, screen, "create table", "CREATE TABLE", "Roboto", 60, "#475F77", "#354B5E", "#D74B4B", 400, 100, (175, 50), 6, 10)
# Création de l'objet gamehistorybutton
gamehistorybutton = Button(largeur_actuelle, hauteur_actuelle, screen, "history", "HISTORY", "Roboto", 70, "#475F77", "#354B5E", "#D74B4B", 300, 500, (1310, 365), 6, 10)
# Création de l'objet deconnexionbutton
deconnexionbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "deconnexion", "LOG OUT", "Roboto", 60, "#475F77", "#354B5E", "#D74B4B", 300, 100, (1605, 970), 6, 10)
# Création de l'objet accountsettingsbutton
accountsettingsbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "account settings", "", "Roboto", 0, "#D74B4B", "#D74B4B", "#D74B4B", 125, 125, (1770, 25), 0, 10,"settinglogo.png")
# Création de l'objet settingpage1button
settingpage1button = Button(largeur_actuelle, hauteur_actuelle, screen, "setting page 1", "PAGE 1", "Roboto", 50, "#475F77", "#354B5E", "#D74B4B", 200, 70, (260, 90), 4, 8)
# Création de l'objet settingpage1button
settingpage2button = Button(largeur_actuelle, hauteur_actuelle, screen, "setting page 2", "PAGE 2", "Roboto", 50, "#475F77", "#354B5E", "#D74B4B", 200, 70, (470, 90), 4, 8)
# Création de l'objet settingpage1button
settingpage3button = Button(largeur_actuelle, hauteur_actuelle, screen, "setting page 3", "PAGE 3", "Roboto", 50, "#475F77", "#354B5E", "#D74B4B", 200, 70, (680, 90), 4, 8)

# Création des scrollboxs
# Création de l'objet serverscrollbox 
serverscrollbox = ScrollBox(210, 215, 1000, 760, server_list)
# Création de l'objet historyscrollbox
historyscrollbox = ScrollBox(210, 215, 1000, 760, server_list)

# Création des TextInputBox
# Création de l'objet tablecodeinput
tablecodeinput = TextInputBox(150, (1360, 790), 400, 100, "#333333", "#888888", 400, False, 6, True)
# Création de l'objet accountpseudoinput
accountpseudoinput = TextInputBox(60, (685, 190), 600, 100, "#333333", "#475F77", 600, False, 10, False, False, "PSEUDO")
# Création de l'objet accountinformationinput
accountinformationinput = TextInputBox(60, (685, 315), 600, 650, "#333333", "#475F77", 600, False, 100, False, False, "INFORMATIONS")

# Création des previews de tables
# Création de l'objet previewlobbys
previewlobbys = Preview_Table((1310, 215))
# Création de l'objet previewhistory
previewhistory = Preview_Table((1310, 215))

# Initialisation de toutes les valeurs globales stockées dans le fichier Global_objects.py
Global_objects.Global_game_state = game_state
Global_objects.Global_accountbutton = accountbutton
Global_objects.Global_playbutton = playbutton
Global_objects.Global_settingsbutton = settingsbutton
Global_objects.Global_exitbutton = exitbutton
Global_objects.Global_backbutton = backbutton
Global_objects.Global_createtablebutton = createtablebutton
Global_objects.Global_gamehistorybutton = gamehistorybutton
Global_objects.Global_deconnexionbutton = deconnexionbutton
Global_objects.Global_accountsettingsbutton = accountsettingsbutton
Global_objects.Global_settingpage1button = settingpage1button
Global_objects.Global_settingpage2button = settingpage2button
Global_objects.Global_settingpage3button = settingpage3button
Global_objects.Global_serverscrollbox = serverscrollbox
Global_objects.Global_historyscrollbox = historyscrollbox
Global_objects.Global_tablecodeinput = tablecodeinput
Global_objects.Global_accountpseudoinput = accountpseudoinput
Global_objects.Global_accountinformationinput = accountinformationinput
Global_objects.Global_previewlobbys = previewlobbys
Global_objects.Global_previewhistory = previewhistory

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