# HUD_State class


import pygame
import sys
import webbrowser
from Screen_adaptation import *
import Global_objects
from Button_class import *
from Scrollbox_class import *
from TextInputBox_class import *
from Preview_Table_class import *


class HUD_State:
    """Classe HUD_State pour gérer l'interface active (https://www.youtube.com/watch?v=j9yMFG3D7fg)
    """

    def __init__(self, largeur_actuelle : int, hauteur_actuelle : int, screen : pygame.Surface, fond : pygame.Surface, logojeu : pygame.Surface, logomwte : pygame.Surface, logomwte_rect : pygame.Rect, pdpplayer : pygame.Surface, table_fond : pygame.Surface, iconmute : pygame.Surface, iconsound : pygame.Surface):
        """Initialisation de l'état de l'interface

        Args:
            largeur_actuelle (int): Largeur de l'écran (pour width_scale())
            hauteur_actuelle (int): Hauteur de l'écran (pour height_scale())
            screen (pygame.Surface): Ecran sur lequel afficher la fenêtre (écran de l'utilisateur)
            fond (pygame.Surface): Fond d'écran
            logojeu (pygame.Surface): Logo du jeu
            logomwte (pygame.Surface): Logo MWTE
            logomwte_rect (pygame.Rect): Partie clickable du logo MWTE
            pdpplayer (pygame.Surface): PDP de l'utilisateur
            table_fond (pygame.Surface): Fond d'écran en jeu
            iconmute (pygame.Surface): Icône bouton MUTE
            iconsound (pygame.Surface): Icône bouton SOUND
        """
        self.fond = fond
        self.logojeu = logojeu
        self.logomwte = logomwte
        self.logomwte_rect = logomwte_rect
        self.pdpplayer = pdpplayer
        self.table_fond = table_fond
        self.largeur_actuelle = largeur_actuelle
        self.hauteur_actuelle = hauteur_actuelle
        self.screen = screen
        # On gére l'icône de son/mute
        self.sound_on = True
        self.iconmute = iconmute
        self.iconsound = iconsound
        # self.state définit l'état actuel de l'interface (qui est par défaut Main Menu)
        self.state = "Main Menu"
        # pile pour le bouton BACK
        self.back_pile = []
        # Savoir si on clique sur quelque chose (utilisable une fois par page sinon ça va se mélanger)
        self.is_pressing = False
        # Placeholder de la description des serveurs lorsqu'on clique dessus
        self.server_test = "Loading ..."
        # Savoir si on affiche ou non le menu des paramètres en jeu pour gérer l'interface
        self.gamesettings = False
        # Page par défaut dans le menu des paramètres
        self.setting_page = 1
        # Valeur par défaut du curseur de volume
        self.cursor_width = width_scale(700, self.largeur_actuelle)
        self.is_setting_volume = False
        # Savoir si une table a été sélectionnée ou non (self.table_selected contient les infos de la table si oui, None si non)
        self.table_selected = None
    
    def mainmenu(self):
        """mainmenu est la fonction qui fait tourner/afficher le menu principal
        """
        # Rassemblement de tout les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Dessine l'image de fond sur le self.screen de l'écran
        self.screen.blit(self.fond, (0, 0))
        # Dessine le logo du jeu
        self.screen.blit(self.logojeu, (width_scale(830, self.largeur_actuelle), height_scale(40, self.hauteur_actuelle)))
        # Dessine le logo MWTE
        self.screen.blit(self.logomwte, self.logomwte_rect)

        # Lien associé au logo MWTE
        # On récupére la position de la souris
        mouse_pos = pygame.mouse.get_pos()
        # On vérifie si la position de la souris est sur le bouton
        if self.logomwte_rect.collidepoint(mouse_pos):
            # On affiche le texte d'information à côté de la souris lorsqu'elle est sur le logo MWTE
            gui_font = pygame.font.SysFont("Roboto", 20, False, True)
            text_surf = gui_font.render("Aller sur le site officiel MWTE", True, "#000000")
            pygame.draw.rect(self.screen, "#FFFFFF", pygame.Rect((mouse_pos[0], mouse_pos[1] + 15), (200, 20)), border_radius = 3)
            self.screen.blit(text_surf, (mouse_pos[0], mouse_pos[1] + 20))
            # On gére le cas où on clique sur le logo pour ouvrir UNE SEULE FOIS notre site web
            if pygame.mouse.get_pressed()[0]:
                self.is_pressing = True
            else:
                if self.is_pressing == True:
                    self.is_pressing = False
                    webbrowser.open("https://mwtestudio.wixsite.com/mwte-studio")
        else:
            self.is_pressing = False
        
        # Affichage des bouttons
        # Cliquer sur le bouton PLAY ouvre l'interface présentant les lobbys disponibles
        Global_objects.playbutton.draw()
        # Cliquer sur le bouton SETTINGS ouvre l'interface présentant les paramètres
        Global_objects.settingsbutton.draw()
        # Cliquer sur le bouton ACCOUNT ouvre l'interface présentant les informations du compte actif
        Global_objects.accountbutton.draw()
        # Affichage des chips de l'utilisateur à droite du bouton ACCOUNT
        gui_font = pygame.font.SysFont("Roboto", width_scale(40, self.largeur_actuelle))
        text_surf = gui_font.render("Chips : ", True, "#FFFFFF")
        pygame.draw.rect(self.screen, "#475F77", pygame.Rect((width_scale(1540, self.largeur_actuelle), height_scale(30, self.hauteur_actuelle)), (width_scale(200, self.largeur_actuelle), height_scale(50, self.hauteur_actuelle))), border_radius = 3)
        self.screen.blit(text_surf, (width_scale(1550, self.largeur_actuelle), height_scale(40, self.hauteur_actuelle)))
        # Cliquer sur le bouton EXIT ferme la fenêtre purement et simplement
        Global_objects.exitbutton.draw()
        # Cliquer sur le bouton GAMES HISTORY affiche l'historique des parties
        Global_objects.gamehistorybutton.draw()

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
            if Global_objects.tablecodeinput.active == True:
                if event.type == pygame.KEYDOWN:
                    # Si on clique sur delete
                    if event.key == pygame.K_BACKSPACE:
                        Global_objects.tablecodeinput.user_text = Global_objects.tablecodeinput.user_text[:-1]
                    # Si on clique sur entrer
                    elif event.key == pygame.K_RETURN:
                        Global_objects.tablecodeinput.user_text = ""
                    # Si on clique sur n'importe quoi d'autre
                    else:
                        # On gère tout les cas de paramètres des objets de la classe TextInputBox (se référer au fichier TextInputBox_class.py pour plus d'informations sur ces paramètres)
                        if Global_objects.tablecodeinput.num_only == True:
                            if event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                if Global_objects.tablecodeinput.max_caracteres > 0:
                                    if len(Global_objects.tablecodeinput.user_text) < Global_objects.tablecodeinput.max_caracteres:
                                        if Global_objects.tablecodeinput.adaptative_size == False:
                                            if Global_objects.tablecodeinput.text_size < Global_objects.tablecodeinput.base_size:
                                                Global_objects.tablecodeinput.user_text += event.unicode
                                        else:
                                            Global_objects.tablecodeinput.user_text += event.unicode
                        else:
                            if Global_objects.tablecodeinput.max_caracteres > 0:
                                if len(Global_objects.tablecodeinput.user_text) < Global_objects.tablecodeinput.max_caracteres:
                                    if Global_objects.tablecodeinput.adaptative_size == False:
                                        if Global_objects.tablecodeinput.text_size < Global_objects.tablecodeinput.base_size:
                                            Global_objects.tablecodeinput.user_text += event.unicode
                                        else:
                                            Global_objects.tablecodeinput.user_text += event.unicode
                                    else:
                                        Global_objects.tablecodeinput.user_text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Molette de la souris vers le haut
                if event.button == 4:
                    Global_objects.serverscrollbox.scroll_up()
                # Molette de la souris vers le bas    
                elif event.button == 5:
                    Global_objects.serverscrollbox.scroll_down()

        # Dessine l'image de fond sur la self.screen de l'écran
        self.screen.blit(self.fond, (0, 0))

        # Dessin de la scrollbox
        Global_objects.serverscrollbox.draw()

        # Affichage des bouttons
        # Cliquer sur le bouton BACK ferme la fenêtre purement et simplement
        Global_objects.backbutton.draw()
        # Cliquer sur le bouton CREER TABLE crée une nouvelle table
        Global_objects.createtablebutton.draw()
        # Cliquer sur le bouton ACCOUNT ouvre l'interface présentant les informations du compte actif
        Global_objects.accountbutton.draw()
        # Affichage des chips de l'utilisateur à droite du bouton ACCOUNT
        gui_font = pygame.font.SysFont("Roboto", width_scale(40, self.largeur_actuelle))
        text_surf = gui_font.render("Chips : ", True, "#FFFFFF")
        pygame.draw.rect(self.screen, "#475F77", pygame.Rect((width_scale(1540, self.largeur_actuelle), height_scale(30, self.hauteur_actuelle)), (width_scale(200, self.largeur_actuelle), height_scale(50, self.hauteur_actuelle))), border_radius = 3)
        self.screen.blit(text_surf, (width_scale(1550, self.largeur_actuelle), height_scale(40, self.hauteur_actuelle)))

        # On crée la box dans laquelle on pourra écrire un code de partie pour rejoindre
        Global_objects.tablecodeinput.draw()
        # On affiche un texte au-dessus de la box qui indique ce que cette dernière fait
        gui_font = pygame.font.SysFont("Roboto", 50)
        text_surf = gui_font.render("Private Table Code", True, "#000000")
        self.screen.blit(text_surf, (width_scale(1370, self.largeur_actuelle), height_scale(850, self.hauteur_actuelle)))

        if self.table_selected is not None:
            # On crée la preview des tables
            Global_objects.previewlobbys.draw()
        
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

        # Dessine l'image de fond sur la self.screen de l'écran (IMPORANT CAR SE SUPERPOSE A L'INTERFACE PRECEDENT ET PERMET DE "L'EFFACER")
        self.screen.blit(self.fond, (0, 0))

        # Affichage des bouttons
        # Cliquer sur le bouton BACK ferme la fenêtre purement et simplement
        Global_objects.backbutton.draw()
        # Cliquer sur le bouton ACCOUNT ouvre l'interface présentant les informations du compte actif
        Global_objects.accountbutton.draw()
        # Affichage des chips de l'utilisateur à droite du bouton ACCOUNT
        gui_font = pygame.font.SysFont("Roboto", width_scale(40, self.largeur_actuelle))
        text_surf = gui_font.render("Chips : ", True, "#FFFFFF")
        pygame.draw.rect(self.screen, "#475F77", pygame.Rect((width_scale(1540, self.largeur_actuelle), height_scale(30, self.hauteur_actuelle)), (width_scale(200, self.largeur_actuelle), height_scale(50, self.hauteur_actuelle))), border_radius = 3)
        self.screen.blit(text_surf, (width_scale(1550, self.largeur_actuelle), height_scale(40, self.hauteur_actuelle)))

        # Affichage des boutons de pages de paramètres
        Global_objects.settingpage1button.draw()
        Global_objects.settingpage2button.draw()
        Global_objects.settingpage3button.draw()
        # Affichage des pages de paramètres avec un arrière-plan noir transparent
        transparent_surface = pygame.Surface((width_scale(1500, self.largeur_actuelle), height_scale(850, self.hauteur_actuelle)), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 128), (0, 0, 1500, 850), border_radius = 5)
        self.screen.blit(transparent_surface, (width_scale(260, self.largeur_actuelle), height_scale(160, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(260, self.largeur_actuelle), height_scale(160, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(260, self.largeur_actuelle), height_scale(160, self.hauteur_actuelle)))
        mouse_pos = pygame.mouse.get_pos()
        # Page 1
        if self.setting_page == 1:
            # Paramètre d'activation/désactivation de la musique
            # Affichage du nom du paramètre VOLUME dans une box
            gui_font = pygame.font.SysFont("Roboto", width_scale(50, self.largeur_actuelle))
            text_surf = gui_font.render("Volume", True, "#FFFFFF")
            pygame.draw.rect(self.screen, "#475F77", pygame.Rect((width_scale(280, self.largeur_actuelle), height_scale(180, self.hauteur_actuelle)), (width_scale(190, self.largeur_actuelle), height_scale(50, self.hauteur_actuelle))), border_radius = 3)
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(190, self.hauteur_actuelle)))
            # On gére l'affichage et les interactions avec l'icône de mute du son
            if self.sound_on is True:
                volume_icon = self.screen.blit(self.iconsound, (width_scale(420, self.largeur_actuelle), height_scale(180, self.hauteur_actuelle)))
            elif self.sound_on is False:
                volume_icon = self.screen.blit(self.iconmute, (width_scale(420, self.largeur_actuelle), height_scale(180, self.hauteur_actuelle)))
            if self.is_setting_volume is False:
                if volume_icon.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:
                        self.is_pressing = True
                    else:
                        if self.is_pressing is True:
                            if self.sound_on is True:
                                self.cursor_width = width_scale(499, self.largeur_actuelle)
                            elif self.sound_on is False:
                                self.cursor_width = width_scale(701, self.largeur_actuelle)
                            self.is_pressing = False
                else:
                    self.is_pressing = False
            # Création du curseur de volume et de la barre derrière
            pygame.draw.rect(self.screen, "#475F77", pygame.Rect((width_scale(500, self.largeur_actuelle), height_scale(200, self.hauteur_actuelle)), (width_scale(200, self.largeur_actuelle), height_scale(10, self.hauteur_actuelle))), border_radius = 6)
            volume_cursor = pygame.draw.circle(self.screen, "#475F77", (self.cursor_width, height_scale(205, self.hauteur_actuelle)), 15)
            # On change la pos x du curseur de volume lorsque l'on clique dessus, sans dépasser les bordures
            if volume_cursor.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    self.is_setting_volume = True
                    Global_objects.buttons_interactibles = False
            # Amélioration de l'interaction avec le curseur
            if self.is_setting_volume is True:
                if not pygame.mouse.get_pressed()[0]:
                    self.is_setting_volume = False
                    Global_objects.buttons_interactibles = True
                else:
                    self.cursor_width = mouse_pos[0]
                    if self.cursor_width > width_scale(700, self.largeur_actuelle):
                        self.cursor_width = width_scale(700, self.largeur_actuelle)
                    elif self.cursor_width < width_scale(500, self.largeur_actuelle):
                        self.cursor_width = width_scale(500, self.largeur_actuelle)
                        self.sound_on = False
                    elif self.cursor_width > width_scale(500, self.largeur_actuelle):
                        self.sound_on = True
            if self.cursor_width > width_scale(700, self.largeur_actuelle):
                self.cursor_width = width_scale(700, self.largeur_actuelle)
            elif self.cursor_width < width_scale(500, self.largeur_actuelle):
                self.cursor_width = width_scale(500, self.largeur_actuelle)
                self.sound_on = False
            elif self.cursor_width > width_scale(500, self.largeur_actuelle):
                self.sound_on = True
            # On récupère le volume actuel
            Global_objects.volume_music = (self.cursor_width - width_scale(500, self.largeur_actuelle)) / (width_scale(700, self.largeur_actuelle) - width_scale(500, self.largeur_actuelle))
        # Page 2
        elif self.setting_page == 2:
            # Temporaire
            gui_font = pygame.font.SysFont("Roboto", 40)
            settingtext_surf = gui_font.render("Page 2 des paramètres", True, "#FFFFFF")
            self.screen.blit(settingtext_surf, (width_scale(270, self.largeur_actuelle), height_scale(170, self.hauteur_actuelle)))
        # Page 3
        elif self.setting_page == 3:
            # Temporaire
            gui_font = pygame.font.SysFont("Roboto", 40)
            settingtext_surf = gui_font.render("Page 3 des paramètres", True, "#FFFFFF")
            self.screen.blit(settingtext_surf, (width_scale(270, self.largeur_actuelle), height_scale(170, self.hauteur_actuelle)))

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
            if Global_objects.accountpseudoinput.active == True:
                if event.type == pygame.KEYDOWN:
                    # Si on clique sur delete
                    if event.key == pygame.K_BACKSPACE:
                        Global_objects.accountpseudoinput.user_text = Global_objects.accountpseudoinput.user_text[:-1]
                    # Si on clique sur entrer
                    elif event.key == pygame.K_RETURN:
                        Global_objects.accountpseudoinput.user_text = ""
                    # Si on clique sur n'importe quoi d'autre
                    else:
                        # On gère tout les cas de paramètres des objets de la classe TextInputBox (se référer au fichier TextInputBox_class.py pour plus d'informations sur ces paramètres)
                        if Global_objects.accountpseudoinput.num_only == True:
                            if event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                if Global_objects.accountpseudoinput.max_caracteres > 0:
                                    if len(Global_objects.accountpseudoinput.user_text) < Global_objects.accountpseudoinput.max_caracteres:
                                        if Global_objects.accountpseudoinput.adaptative_size == False:
                                            if Global_objects.accountpseudoinput.text_size < Global_objects.accountpseudoinput.base_size:
                                                Global_objects.accountpseudoinput.user_text += event.unicode
                                        else:
                                            Global_objects.accountpseudoinput.user_text += event.unicode
                        else:
                            if Global_objects.accountpseudoinput.max_caracteres > 0:
                                if len(Global_objects.accountpseudoinput.user_text) < Global_objects.accountpseudoinput.max_caracteres:
                                    if Global_objects.accountpseudoinput.adaptative_size == False:
                                        if Global_objects.accountpseudoinput.text_size < Global_objects.accountpseudoinput.base_size:
                                            Global_objects.accountpseudoinput.user_text += event.unicode
                                        else:
                                            Global_objects.accountpseudoinput.user_text += event.unicode
                                    else:
                                        Global_objects.accountpseudoinput.user_text += event.unicode
            # Si on a sélectionne la accountpseudoinput
            if Global_objects.accountinformationinput.active == True:
                if event.type == pygame.KEYDOWN:
                    # Si on clique sur delete
                    if event.key == pygame.K_BACKSPACE:
                        Global_objects.accountinformationinput.user_text = Global_objects.accountinformationinput.user_text[:-1]
                    # Si on clique sur entrer
                    elif event.key == pygame.K_RETURN:
                        Global_objects.accountinformationinput.user_text = ""
                    # Si on clique sur n'importe quoi d'autre
                    else:
                        # On gère tout les cas de paramètres des objets de la classe TextInputBox (se référer au fichier TextInputBox_class.py pour plus d'informations sur ces paramètres)
                        if Global_objects.accountinformationinput.num_only == True:
                            if event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                if Global_objects.accountinformationinput.max_caracteres > 0:
                                    if len(Global_objects.accountinformationinput.user_text) < Global_objects.accountinformationinput.max_caracteres:
                                        if Global_objects.accountinformationinput.adaptative_size == False:
                                            if Global_objects.accountinformationinput.text_size < Global_objects.accountinformationinput.base_size:
                                                Global_objects.accountinformationinput.user_text += event.unicode
                                        else:
                                            Global_objects.accountinformationinput.user_text += event.unicode
                        else:
                            if Global_objects.accountinformationinput.max_caracteres > 0:
                                if len(Global_objects.accountinformationinput.user_text) < Global_objects.accountinformationinput.max_caracteres:
                                    if Global_objects.accountinformationinput.adaptative_size == False:
                                        if Global_objects.accountinformationinput.text_size < Global_objects.accountinformationinput.base_size:
                                            Global_objects.accountinformationinput.user_text += event.unicode
                                        else:
                                            Global_objects.accountinformationinput.user_text += event.unicode
                                    else:
                                        Global_objects.accountinformationinput.user_text += event.unicode


        # Dessine l'image de fond sur la self.screen de l'écran (IMPORANT CAR SE SUPERPOSE A L'INTERFACE PRECEDENT ET PERMET DE "L'EFFACER")
        self.screen.blit(self.fond, (0, 0))

        # Affichage des bouttons
        # Cliquer sur le bouton BACK ferme la fenêtre purement et simplement
        Global_objects.backbutton.draw()

        # Dessin des infos du compte
        # Affichage de la pdp de l'utilisateur
        self.screen.blit(self.pdpplayer, (width_scale(360, self.largeur_actuelle), height_scale(190, self.hauteur_actuelle)))
        # Affichage des chips de l'utilisateur
        gui_font = pygame.font.SysFont("Roboto", width_scale(40, self.largeur_actuelle))
        text_surf = gui_font.render("Chips : ", True, "#FFFFFF")
        pygame.draw.rect(self.screen, "#475F77", pygame.Rect((width_scale(400, self.largeur_actuelle), height_scale(465, self.hauteur_actuelle)), (width_scale(225, self.largeur_actuelle), height_scale(50, self.hauteur_actuelle))), border_radius = 3)
        self.screen.blit(text_surf, (width_scale(410, self.largeur_actuelle), height_scale(475, self.hauteur_actuelle)))
        # Affichage du pseudo de l'utilisateur
        Global_objects.accountpseudoinput.draw()
        # Affichage des infos de l'utilisateur
        Global_objects.accountinformationinput.draw()
        # Affichage du bouton de déconnexion de l'utilisateur
        Global_objects.deconnexionbutton.draw()
        # Affichage du bouton de paramètres du compte de l'utilisateur
        Global_objects.accountsettingsbutton.draw()
        
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
                    Global_objects.historyscrollbox.scroll_up()
                # Molette de la souris vers le bas    
                elif event.button == 5:
                    Global_objects.historyscrollbox.scroll_down()

        # Dessine l'image de fond sur la self.screen de l'écran (IMPORANT CAR SE SUPERPOSE A L'INTERFACE PRECEDENT ET PERMET DE "L'EFFACER")
        self.screen.blit(self.fond, (0, 0))

        # Dessin de la scrollbox
        Global_objects.historyscrollbox.draw()  

        # On crée la preview des tables
        Global_objects.previewhistory.draw()

        # Affichage des bouttons
        # Cliquer sur le bouton BACK ferme la fenêtre purement et simplement
        Global_objects.backbutton.draw()
        # Cliquer sur le bouton ACCOUNT ouvre l'interface présentant les informations du compte actif
        Global_objects.accountbutton.draw()
        # Affichage des chips de l'utilisateur à droite du bouton ACCOUNT
        gui_font = pygame.font.SysFont("Roboto", width_scale(40, self.largeur_actuelle))
        text_surf = gui_font.render("Chips : ", True, "#FFFFFF")
        pygame.draw.rect(self.screen, "#475F77", pygame.Rect((width_scale(1540, self.largeur_actuelle), height_scale(30, self.hauteur_actuelle)), (width_scale(200, self.largeur_actuelle), height_scale(50, self.hauteur_actuelle))), border_radius = 3)
        self.screen.blit(text_surf, (width_scale(1550, self.largeur_actuelle), height_scale(40, self.hauteur_actuelle)))

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

        # Dessine l'image de fond sur la self.screen de l'écran (IMPORANT CAR SE SUPERPOSE A L'INTERFACE PRECEDENT ET PERMET DE "L'EFFACER")
        self.screen.fill("green")
        self.screen.blit(self.table_fond, (0, 0))

        # Affichage des infos de la table sélectionnée en placeholder
        gui_font = pygame.font.SysFont("Roboto", width_scale(40, self.largeur_actuelle))
        text_surf = gui_font.render(self.server_test, True, "#FFFFFF")
        self.screen.blit(text_surf, (width_scale(510, self.largeur_actuelle), height_scale(510, self.hauteur_actuelle)))

        # Affichage de la zone qui comportera les actions du joueur
        # Fond noir
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect((width_scale(1500, self.largeur_actuelle), 0), (width_scale(420, self.largeur_actuelle), self.hauteur_actuelle)))
        # Boutons d'actions
        Global_objects.checkbutton.draw()
        Global_objects.callbutton.draw()
        Global_objects.laybutton.draw()
        Global_objects.raisebutton.draw()

        # TOUT CE QUI EST EN DESSOUS DE CE BLOC NE SERA PAS DESSINE DERRIERE LA SURFACE TRANSPARENTE
        # Quand l'utilisateur clique sur le bouton des paramètres
        if self.gamesettings == True:
            self.setting_background_surface = pygame.Surface((self.largeur_actuelle, self.hauteur_actuelle), pygame.SRCALPHA)
            pygame.draw.rect(self.setting_background_surface, (220, 220, 220, 75), (0, 0, self.largeur_actuelle, self.hauteur_actuelle))
            self.screen.blit(self.setting_background_surface, (0, 0))
            # Cliquer sur le bouton BACK ferme la fenêtre purement et simplement
            Global_objects.backbutton.draw()

        # Affichage des bouttons
        # Cliquer sur le bouton gamesettingsbutton affiche un menu de paramètres rapides pendant la partie
        Global_objects.gamesettingsbutton.draw()

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