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
from Sits_class import *
from Check_click import *
import time



class HUD_State:
    """Classe HUD_State pour gérer l'interface active (https://www.youtube.com/watch?v=j9yMFG3D7fg)
    """

    def __init__(self, largeur_actuelle : int, hauteur_actuelle : int, screen : pygame.Surface, fond : pygame.Surface, logojeu : pygame.Surface, logomwte : pygame.Surface, logomwte_rect : pygame.Rect, pdpplayer : pygame.Surface, table_fond : pygame.Surface, sounds_icons : list):
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
            sounds_icons (list): Liste contenant les icônes de son ([0] = mute, [1] = son bas, [2] = son moyen, [3] = son fort)
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
        # On gére les icônes de son
        self.sound_on = True
        self.sounds_icons = sounds_icons
        self.last_sound = 690
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
        self.cursor_width = width_scale(690, self.largeur_actuelle)
        self.is_setting_volume = False
        # Savoir si une table a été sélectionnée ou non (self.table_selected contient les infos de la table si oui, None si non)
        self.table_selected = None
        # Savoir si le code entré dans lobby est valide, et laisser afficher 2 secondes l'erreur
        self.error = [False, 0]
    
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
        self.screen.blit(self.logojeu, (width_scale(580, self.largeur_actuelle), height_scale(-50, self.hauteur_actuelle)))
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
                        # On essaie de rejoindre la partie avec le code entré
                        try:
                            a = "a" - 8
                            print(a)
                            lobby_id = int(Global_objects.tablecodeinput.user_text)
                            ask_sits_infos(Global_objects.client_socket,lobby_id)
                            if True: #Plus tard la vérification de l'existance du lobby
                                time.sleep(0.2)
                                Global_objects.game_state.server_test = Global_objects.tablecodeinput.user_text
                                Global_objects.game_state.back_pile = ["Main Menu"]
                                Global_objects.game_state.state = "Game Menu"
                                Global_objects.game_state.table_selected = None
                                if len(Global_objects.previewlobbys.players) == 1:
                                    Global_objects.sit_1.player = Global_objects.previewlobbys.players[0]
                                if len(Global_objects.previewlobbys.players) == 2:
                                    Global_objects.sit_1.player = Global_objects.previewlobbys.players[0]
                                    Global_objects.sit_2.player = Global_objects.previewlobbys.players[1]
                                if len(Global_objects.previewlobbys.players) == 3:
                                    Global_objects.sit_1.player = Global_objects.previewlobbys.players[0]
                                    Global_objects.sit_2.player = Global_objects.previewlobbys.players[1]
                                    Global_objects.sit_3.player = Global_objects.previewlobbys.players[2]
                                if len(Global_objects.previewlobbys.players) == 4:
                                    Global_objects.sit_1.player = Global_objects.previewlobbys.players[0]
                                    Global_objects.sit_2.player = Global_objects.previewlobbys.players[1]
                                    Global_objects.sit_3.player = Global_objects.previewlobbys.players[2]
                                    Global_objects.sit_4.player = Global_objects.previewlobbys.players[3]
                                if len(Global_objects.previewlobbys.players) == 5:
                                    Global_objects.sit_1.player = Global_objects.previewlobbys.players[0]
                                    Global_objects.sit_2.player = Global_objects.previewlobbys.players[1]
                                    Global_objects.sit_3.player = Global_objects.previewlobbys.players[2]
                                    Global_objects.sit_4.player = Global_objects.previewlobbys.players[3]
                                    Global_objects.sit_5.player = Global_objects.previewlobbys.players[4]
                                if len(Global_objects.previewlobbys.players) == 6:
                                    Global_objects.sit_1.player = Global_objects.previewlobbys.players[0]
                                    Global_objects.sit_2.player = Global_objects.previewlobbys.players[1]
                                    Global_objects.sit_3.player = Global_objects.previewlobbys.players[2]
                                    Global_objects.sit_4.player = Global_objects.previewlobbys.players[3]
                                    Global_objects.sit_5.player = Global_objects.previewlobbys.players[4]
                                    Global_objects.sit_6.player = Global_objects.previewlobbys.players[5]
                                if len(Global_objects.previewlobbys.players) == 7:
                                    Global_objects.sit_1.player = Global_objects.previewlobbys.players[0]
                                    Global_objects.sit_2.player = Global_objects.previewlobbys.players[1]
                                    Global_objects.sit_3.player = Global_objects.previewlobbys.players[2]
                                    Global_objects.sit_4.player = Global_objects.previewlobbys.players[3]
                                    Global_objects.sit_5.player = Global_objects.previewlobbys.players[4]
                                    Global_objects.sit_6.player = Global_objects.previewlobbys.players[5]
                                    Global_objects.sit_7.player = Global_objects.previewlobbys.players[6]
                                if len(Global_objects.previewlobbys.players) == 8:
                                    Global_objects.sit_1.player = Global_objects.previewlobbys.players[0]
                                    Global_objects.sit_2.player = Global_objects.previewlobbys.players[1]
                                    Global_objects.sit_3.player = Global_objects.previewlobbys.players[2]
                                    Global_objects.sit_4.player = Global_objects.previewlobbys.players[3]
                                    Global_objects.sit_5.player = Global_objects.previewlobbys.players[4]
                                    Global_objects.sit_6.player = Global_objects.previewlobbys.players[5]
                                    Global_objects.sit_7.player = Global_objects.previewlobbys.players[6]
                                    Global_objects.sit_8.player = Global_objects.previewlobbys.players[7]
                                if len(Global_objects.previewlobbys.players) == 9:
                                    Global_objects.sit_1.player = Global_objects.previewlobbys.players[0]
                                    Global_objects.sit_2.player = Global_objects.previewlobbys.players[1]
                                    Global_objects.sit_3.player = Global_objects.previewlobbys.players[2]
                                    Global_objects.sit_4.player = Global_objects.previewlobbys.players[3]
                                    Global_objects.sit_5.player = Global_objects.previewlobbys.players[4]
                                    Global_objects.sit_6.player = Global_objects.previewlobbys.players[5]
                                    Global_objects.sit_7.player = Global_objects.previewlobbys.players[6]
                                    Global_objects.sit_8.player = Global_objects.previewlobbys.players[7]
                                    Global_objects.sit_9.player = Global_objects.previewlobbys.players[8]
                                if len(Global_objects.previewlobbys.players) == 10:
                                    Global_objects.sit_1.player = Global_objects.previewlobbys.players[0]
                                    Global_objects.sit_2.player = Global_objects.previewlobbys.players[1]
                                    Global_objects.sit_3.player = Global_objects.previewlobbys.players[2]
                                    Global_objects.sit_4.player = Global_objects.previewlobbys.players[3]
                                    Global_objects.sit_5.player = Global_objects.previewlobbys.players[4]
                                    Global_objects.sit_6.player = Global_objects.previewlobbys.players[5]
                                    Global_objects.sit_7.player = Global_objects.previewlobbys.players[6]
                                    Global_objects.sit_8.player = Global_objects.previewlobbys.players[7]
                                    Global_objects.sit_9.player = Global_objects.previewlobbys.players[8]
                                    Global_objects.sit_10.player = Global_objects.previewlobbys.players[9]
                            else:
                                pass
                        except:
                            self.error[0] = True
                            self.error[1] = time.time()
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
        # Cliquer sur le bouton BACK retourne une page en arrière
        Global_objects.backbutton.draw()
        # Cliquer sur le bouton CREER TABLE crée une nouvelle table
        Global_objects.createtablebutton.draw()
        # Cliquer sur le bouton REFRESH réactualise les lobbys affichés
        Global_objects.refreshbutton.draw()
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

        if not self.table_selected is None:
            # On crée la preview des tables
            Global_objects.previewlobbys.draw()
        
        if self.error[0] is True:
            # Affichage d'un message d'erreur dans le cas où le code de lobby n'existe pas
            gui_font = pygame.font.SysFont("Roboto", width_scale(70, self.largeur_actuelle))
            text_surf = gui_font.render("ERROR : NO GAME FOUND", True, "#FFFFFF")
            pygame.draw.rect(self.screen, "#FF0000", pygame.Rect((width_scale(650, self.largeur_actuelle), height_scale(400, self.hauteur_actuelle)), (width_scale(650, self.largeur_actuelle), height_scale(100, self.hauteur_actuelle))), border_radius = 2)
            self.screen.blit(text_surf, (width_scale(655, self.largeur_actuelle), height_scale(430, self.hauteur_actuelle)))
            # On vérifie si le message est là depuis plus de 2 secondes et dans ce cas on l'efface
            if self.error[1] - time.time() <= -1:
                self.error[0] = False


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
        # Cliquer sur le bouton BACK retourne une page en arrière
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
            pygame.draw.rect(self.screen, "#0000E0", pygame.Rect((width_scale(280, self.largeur_actuelle), height_scale(180, self.hauteur_actuelle)), (width_scale(450, self.largeur_actuelle), height_scale(50, self.hauteur_actuelle))), border_radius = 3)
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(190, self.hauteur_actuelle)))
            # On gére l'affichage avec les icônes de son
            if self.cursor_width <= width_scale(490, self.largeur_actuelle) or self.sound_on is False:
                volume_icon = self.screen.blit(self.sounds_icons[0], (width_scale(415, self.largeur_actuelle), height_scale(172, self.hauteur_actuelle)))
            elif self.cursor_width > width_scale(490, self.largeur_actuelle) and self.cursor_width <= width_scale(556, self.largeur_actuelle):
                volume_icon = self.screen.blit(self.sounds_icons[1], (width_scale(415, self.largeur_actuelle), height_scale(172, self.hauteur_actuelle)))
            elif self.cursor_width > width_scale(556, self.largeur_actuelle) and self.cursor_width <= width_scale(622, self.largeur_actuelle):
                volume_icon = self.screen.blit(self.sounds_icons[2], (width_scale(415, self.largeur_actuelle), height_scale(172, self.hauteur_actuelle)))
            elif self.cursor_width > width_scale(622, self.largeur_actuelle) and self.cursor_width <= width_scale(690, self.largeur_actuelle):
                volume_icon = self.screen.blit(self.sounds_icons[3], (width_scale(415, self.largeur_actuelle), height_scale(172, self.hauteur_actuelle)))
            # On gére l'utilisation/les interactions avec le bouton de son
            if self.is_setting_volume is False:
                if volume_icon.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:
                        self.is_pressing = True
                    else:
                        if self.is_pressing is True:
                            if self.sound_on is True:
                                self.last_sound = self.cursor_width
                                self.cursor_width = width_scale(490, self.largeur_actuelle)
                                self.sound_on = False
                            elif self.sound_on is False:
                                self.cursor_width = self.last_sound
                                self.sound_on = True
                            self.is_pressing = False
                else:
                    self.is_pressing = False
            # Création du curseur de volume et de la barre derrière
            volume_bar = pygame.draw.rect(self.screen, "#FFFFFF", pygame.Rect((width_scale(490, self.largeur_actuelle), height_scale(200, self.hauteur_actuelle)), (width_scale(200, self.largeur_actuelle), height_scale(10, self.hauteur_actuelle))), border_radius = 6)
            volume_cursor = pygame.draw.circle(self.screen, "#FFFFFF", (self.cursor_width, height_scale(205, self.hauteur_actuelle)), 15)
            # On change la pos x du curseur de volume lorsque l'on clique dessus, sans dépasser les bordures
            if volume_cursor.collidepoint(mouse_pos) or volume_bar.collidepoint(mouse_pos):
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
                    # On gére les cas où l'utilisateur pousserait le curseur en dehors de la barre de son
                    if self.cursor_width >= width_scale(690, self.largeur_actuelle):
                        self.cursor_width = width_scale(690, self.largeur_actuelle)
                    elif self.cursor_width <= width_scale(490, self.largeur_actuelle):
                        self.cursor_width = width_scale(490, self.largeur_actuelle)
                        self.sound_on = False
                    elif self.cursor_width > width_scale(490, self.largeur_actuelle):
                        self.sound_on = True
            # On vérifie en dehors du if les cas où l'utilisateur pousserait le curseur en dehors de la barre de son
            if self.cursor_width >= width_scale(690, self.largeur_actuelle):
                self.cursor_width = width_scale(690, self.largeur_actuelle)
            elif self.cursor_width <= width_scale(490, self.largeur_actuelle):
                self.cursor_width = width_scale(490, self.largeur_actuelle)
                self.sound_on = False
            elif self.cursor_width > width_scale(490, self.largeur_actuelle):
                self.sound_on = True
            # On récupère le volume actuel
            Global_objects.volume_music = (self.cursor_width - width_scale(490, self.largeur_actuelle)) / (width_scale(690, self.largeur_actuelle) - width_scale(490, self.largeur_actuelle))
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
        # Cliquer sur le bouton BACK retourne une page en arrière
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
        # Cliquer sur le bouton BACK retourne une page en arrière
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

    def createtable(self):
        """createtable est la fonction qui fait tourner/afficher l'interface de création de partie
        """
        # Rassemblement de tout les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Dessine l'image de fond sur la self.screen de l'écran (IMPORANT CAR SE SUPERPOSE A L'INTERFACE PRECEDENT ET PERMET DE "L'EFFACER")
        self.screen.blit(self.table_fond, (0, 0))

        # Affichage des bouttons
        # Cliquer sur le bouton BACK retourne une page en arrière
        Global_objects.backbutton.draw()
        # Cliquer sur le bouton ACCOUNT ouvre l'interface présentant les informations du compte actif
        Global_objects.accountbutton.draw()
        # Affichage des chips de l'utilisateur à droite du bouton ACCOUNT
        gui_font = pygame.font.SysFont("Roboto", width_scale(40, self.largeur_actuelle))
        text_surf = gui_font.render("Chips : ", True, "#FFFFFF")
        pygame.draw.rect(self.screen, "#475F77", pygame.Rect((width_scale(1540, self.largeur_actuelle), height_scale(30, self.hauteur_actuelle)), (width_scale(200, self.largeur_actuelle), height_scale(50, self.hauteur_actuelle))), border_radius = 3)
        self.screen.blit(text_surf, (width_scale(1550, self.largeur_actuelle), height_scale(40, self.hauteur_actuelle)))

        # Affichage d'un arrière-plan noir transparent derrière chaque paramètre de la partie à selectionner
        transparent_surface = pygame.Surface((width_scale(450, self.largeur_actuelle), height_scale(100, self.hauteur_actuelle)), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 128), (0, 0, 450, 100), border_radius = 5)
        self.screen.blit(transparent_surface, (width_scale(180, self.largeur_actuelle), height_scale(110, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(180, self.largeur_actuelle), height_scale(260, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(180, self.largeur_actuelle), height_scale(410, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(180, self.largeur_actuelle), height_scale(560, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(180, self.largeur_actuelle), height_scale(710, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(180, self.largeur_actuelle), height_scale(860, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(740, self.largeur_actuelle), height_scale(110, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(740, self.largeur_actuelle), height_scale(260, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(740, self.largeur_actuelle), height_scale(410, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(740, self.largeur_actuelle), height_scale(560, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(740, self.largeur_actuelle), height_scale(710, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(740, self.largeur_actuelle), height_scale(860, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(1300, self.largeur_actuelle), height_scale(110, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(1300, self.largeur_actuelle), height_scale(260, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(1300, self.largeur_actuelle), height_scale(410, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(1300, self.largeur_actuelle), height_scale(560, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(1300, self.largeur_actuelle), height_scale(710, self.hauteur_actuelle)))
        self.screen.blit(transparent_surface, (width_scale(1300, self.largeur_actuelle), height_scale(860, self.hauteur_actuelle)))

        # Met à jour l'affichage de l'interface
        pygame.display.update()

    def gamemenu(self):
        """game est la fonction qui fait tourner/afficher l'interface en jeu
        """
        # Rassemblement de tout les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fond noir
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect((0, 0), (self.largeur_actuelle, self.hauteur_actuelle)))
        # Dessine l'image de fond sur la self.screen de l'écran (IMPORANT CAR SE SUPERPOSE A L'INTERFACE PRECEDENT ET PERMET DE "L'EFFACER")
        table_fond = pygame.transform.scale(self.table_fond, (self.largeur_actuelle, height_scale(980, self.hauteur_actuelle)))
        self.screen.blit(table_fond, (0, 0))

        # Affichage des infos de la table sélectionnée en placeholder
        gui_font = pygame.font.SysFont("Roboto", width_scale(40, self.largeur_actuelle))
        text_surf = gui_font.render(self.server_test, True, "#FFFFFF")
        self.screen.blit(text_surf, (width_scale(510, self.largeur_actuelle), height_scale(510, self.hauteur_actuelle)))

        # Affichage de la zone qui comportera les actions du joueur
        # Boutons d'actions
        Global_objects.checkbutton.draw()
        Global_objects.callbutton.draw()
        Global_objects.foldbutton.draw()
        Global_objects.raisebutton.draw()
        match len(Global_objects.previewlobbys.players):

            case 2:
                Global_objects.sit_1.x = width_scale(840, self.largeur_actuelle)
                Global_objects.sit_1.y = height_scale(200, self.hauteur_actuelle)
                Global_objects.sit_1.draw()
                Global_objects.sit_2.x = width_scale(840, self.largeur_actuelle)
                Global_objects.sit_2.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_2.draw()

            case 3:
                Global_objects.sit_1.x = width_scale(840, self.largeur_actuelle)
                Global_objects.sit_1.y = height_scale(200, self.hauteur_actuelle)
                Global_objects.sit_1.draw()
                Global_objects.sit_2.x = width_scale(540, self.largeur_actuelle)
                Global_objects.sit_2.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_2.draw()
                Global_objects.sit_3.x = width_scale(1140, self.largeur_actuelle)
                Global_objects.sit_3.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_3.draw()

            case 4:
                Global_objects.sit_1.x = width_scale(840, self.largeur_actuelle)
                Global_objects.sit_1.y = height_scale(200, self.hauteur_actuelle)
                Global_objects.sit_1.draw()
                Global_objects.sit_2.x = width_scale(1300, self.largeur_actuelle)
                Global_objects.sit_2.y = height_scale(450, self.hauteur_actuelle)
                Global_objects.sit_2.draw()
                Global_objects.sit_3.x = width_scale(840, self.largeur_actuelle)
                Global_objects.sit_3.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_3.draw()
                Global_objects.sit_4.x = width_scale(380, self.largeur_actuelle)
                Global_objects.sit_4.y = height_scale(450, self.hauteur_actuelle)
                Global_objects.sit_4.draw()

            case 5:
                Global_objects.sit_1.x = width_scale(840, self.largeur_actuelle)
                Global_objects.sit_1.y = height_scale(200, self.hauteur_actuelle)
                Global_objects.sit_1.draw()
                Global_objects.sit_2.x = width_scale(1300, self.largeur_actuelle)
                Global_objects.sit_2.y = height_scale(450, self.hauteur_actuelle)
                Global_objects.sit_2.draw()
                Global_objects.sit_3.x = width_scale(1140, self.largeur_actuelle)
                Global_objects.sit_3.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_3.draw()
                Global_objects.sit_4.x = width_scale(540, self.largeur_actuelle)
                Global_objects.sit_4.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_4.draw()
                Global_objects.sit_5.x = width_scale(380, self.largeur_actuelle)
                Global_objects.sit_5.y = height_scale(450, self.hauteur_actuelle)
                Global_objects.sit_5.draw()

            case 6:
                Global_objects.sit_1.x = width_scale(540, self.largeur_actuelle)
                Global_objects.sit_1.y = height_scale(200, self.hauteur_actuelle)
                Global_objects.sit_1.draw()
                Global_objects.sit_2.x = width_scale(1140, self.largeur_actuelle)
                Global_objects.sit_2.y = height_scale(200, self.hauteur_actuelle)
                Global_objects.sit_2.draw()
                Global_objects.sit_3.x = width_scale(1300, self.largeur_actuelle)
                Global_objects.sit_3.y = height_scale(450, self.hauteur_actuelle)
                Global_objects.sit_3.draw()
                Global_objects.sit_4.x = width_scale(1140, self.largeur_actuelle)
                Global_objects.sit_4.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_4.draw()
                Global_objects.sit_5.x = width_scale(540, self.largeur_actuelle)
                Global_objects.sit_5.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_5.draw()
                Global_objects.sit_6.x = width_scale(380, self.largeur_actuelle)
                Global_objects.sit_6.y = height_scale(450, self.hauteur_actuelle)
                Global_objects.sit_6.draw()

            case 7:
                Global_objects.sit_1.x = width_scale(840, self.largeur_actuelle)
                Global_objects.sit_1.y = height_scale(200, self.hauteur_actuelle)
                Global_objects.sit_1.draw()
                Global_objects.sit_2.x = width_scale(1300, self.largeur_actuelle)
                Global_objects.sit_2.y = height_scale(350, self.hauteur_actuelle)
                Global_objects.sit_2.draw()
                Global_objects.sit_3.x = width_scale(1300, self.largeur_actuelle)
                Global_objects.sit_3.y = height_scale(550, self.hauteur_actuelle)
                Global_objects.sit_3.draw()
                Global_objects.sit_4.x = width_scale(1080, self.largeur_actuelle)
                Global_objects.sit_4.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_4.draw()
                Global_objects.sit_5.x = width_scale(610, self.largeur_actuelle)
                Global_objects.sit_5.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_5.draw()
                Global_objects.sit_6.x = width_scale(380, self.largeur_actuelle)
                Global_objects.sit_6.y = height_scale(550, self.hauteur_actuelle)
                Global_objects.sit_6.draw()
                Global_objects.sit_7.x = width_scale(380, self.largeur_actuelle)
                Global_objects.sit_7.y = height_scale(350, self.hauteur_actuelle)
                Global_objects.sit_7.draw()

            case 8:
                Global_objects.sit_1.x = width_scale(610, self.largeur_actuelle)
                Global_objects.sit_1.y = height_scale(200, self.hauteur_actuelle)
                Global_objects.sit_1.draw()
                Global_objects.sit_2.x = width_scale(1080, self.largeur_actuelle)
                Global_objects.sit_2.y = height_scale(200, self.hauteur_actuelle)
                Global_objects.sit_2.draw()
                Global_objects.sit_3.x = width_scale(1300, self.largeur_actuelle)
                Global_objects.sit_3.y = height_scale(350, self.hauteur_actuelle)
                Global_objects.sit_3.draw()
                Global_objects.sit_4.x = width_scale(1300, self.largeur_actuelle)
                Global_objects.sit_4.y = height_scale(550, self.hauteur_actuelle)
                Global_objects.sit_4.draw()
                Global_objects.sit_5.x = width_scale(1080, self.largeur_actuelle)
                Global_objects.sit_5.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_5.draw()
                Global_objects.sit_6.x = width_scale(610, self.largeur_actuelle)
                Global_objects.sit_6.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_6.draw()
                Global_objects.sit_7.x = width_scale(380, self.largeur_actuelle)
                Global_objects.sit_7.y = height_scale(550, self.hauteur_actuelle)
                Global_objects.sit_7.draw()
                Global_objects.sit_8.x = width_scale(380, self.largeur_actuelle)
                Global_objects.sit_8.y = height_scale(350, self.hauteur_actuelle)
                Global_objects.sit_8.draw()

            case 9:
                Global_objects.sit_1.x = width_scale(840, self.largeur_actuelle)
                Global_objects.sit_1.y = height_scale(100, self.hauteur_actuelle)
                Global_objects.sit_1.draw()
                Global_objects.sit_2.x = width_scale(1140, self.largeur_actuelle)
                Global_objects.sit_2.y = height_scale(250, self.hauteur_actuelle)
                Global_objects.sit_2.draw()
                Global_objects.sit_3.x = width_scale(1360, self.largeur_actuelle)
                Global_objects.sit_3.y = height_scale(400, self.hauteur_actuelle)
                Global_objects.sit_3.draw()
                Global_objects.sit_4.x = width_scale(1360, self.largeur_actuelle)
                Global_objects.sit_4.y = height_scale(600, self.hauteur_actuelle)
                Global_objects.sit_4.draw()
                Global_objects.sit_5.x = width_scale(1080, self.largeur_actuelle)
                Global_objects.sit_5.y = height_scale(750, self.hauteur_actuelle)
                Global_objects.sit_5.draw()
                Global_objects.sit_6.x = width_scale(610, self.largeur_actuelle)
                Global_objects.sit_6.y = height_scale(750, self.hauteur_actuelle)
                Global_objects.sit_6.draw()
                Global_objects.sit_7.x = width_scale(320, self.largeur_actuelle)
                Global_objects.sit_7.y = height_scale(600, self.hauteur_actuelle)
                Global_objects.sit_7.draw()
                Global_objects.sit_8.x = width_scale(320, self.largeur_actuelle)
                Global_objects.sit_8.y = height_scale(400, self.hauteur_actuelle)
                Global_objects.sit_8.draw()
                Global_objects.sit_9.x = width_scale(540, self.largeur_actuelle)
                Global_objects.sit_9.y = height_scale(250, self.hauteur_actuelle)
                Global_objects.sit_9.draw()

            case 10:
                Global_objects.sit_1.x = width_scale(610, self.largeur_actuelle)
                Global_objects.sit_1.y = height_scale(100, self.hauteur_actuelle)
                Global_objects.sit_1.draw()
                Global_objects.sit_2.x = width_scale(1080, self.largeur_actuelle)
                Global_objects.sit_2.y = height_scale(100, self.hauteur_actuelle)
                Global_objects.sit_2.draw()
                Global_objects.sit_3.x = width_scale(1240, self.largeur_actuelle)
                Global_objects.sit_3.y = height_scale(250, self.hauteur_actuelle)
                Global_objects.sit_3.draw()
                Global_objects.sit_4.x = width_scale(1400, self.largeur_actuelle)
                Global_objects.sit_4.y = height_scale(400, self.hauteur_actuelle)
                Global_objects.sit_4.draw()
                Global_objects.sit_5.x = width_scale(1240, self.largeur_actuelle)
                Global_objects.sit_5.y = height_scale(600, self.hauteur_actuelle)
                Global_objects.sit_5.draw()
                Global_objects.sit_6.x = width_scale(1080, self.largeur_actuelle)
                Global_objects.sit_6.y = height_scale(750, self.hauteur_actuelle)
                Global_objects.sit_6.draw()
                Global_objects.sit_7.x = width_scale(610, self.largeur_actuelle)
                Global_objects.sit_7.y = height_scale(750, self.hauteur_actuelle)
                Global_objects.sit_7.draw()
                Global_objects.sit_8.x = width_scale(440, self.largeur_actuelle)
                Global_objects.sit_8.y = height_scale(600, self.hauteur_actuelle)
                Global_objects.sit_8.draw()
                Global_objects.sit_9.x = width_scale(280, self.largeur_actuelle)
                Global_objects.sit_9.y = height_scale(400, self.hauteur_actuelle)
                Global_objects.sit_9.draw()
                Global_objects.sit_10.x = width_scale(440, self.largeur_actuelle)
                Global_objects.sit_10.y = height_scale(250, self.hauteur_actuelle)
                Global_objects.sit_10.draw()

        # TOUT CE QUI EST EN DESSOUS DE CE BLOC NE SERA PAS DESSINE DERRIERE LA SURFACE TRANSPARENTE
        # Quand l'utilisateur clique sur le bouton des paramètres
        if self.gamesettings == True:
            self.setting_background_surface = pygame.Surface((self.largeur_actuelle, self.hauteur_actuelle), pygame.SRCALPHA)
            pygame.draw.rect(self.setting_background_surface, (220, 220, 220, 75), (0, 0, self.largeur_actuelle, self.hauteur_actuelle))
            self.screen.blit(self.setting_background_surface, (0, 0))
            # Cliquer sur le bouton BACK retourne au menu principal
            Global_objects.backbutton.draw()

        # Affichage des bouttons
        # Cliquer sur le bouton gamesettingsbutton affiche un menu de paramètres rapides pendant la partie
        Global_objects.gamesettingsbutton.draw()

        # Met à jour l'affichage de l'interface
        pygame.display.update()
    
    def state_manager(self):
        """state_manager se charge d'afficher la bonne interface en fonction de l'état de self.state
        """
        match self.state:
            case "Main Menu":
                self.mainmenu()
            case "Lobby Menu":
                self.lobbymenu()
            case "Setting Menu":
                self.settingmenu()
            case "Account Menu":
                self.accountmenu()
            case "History Menu":
                self.historymenu()
            case "Create Menu":
                self.createtable()
            case "Game Menu":
                self.gamemenu()