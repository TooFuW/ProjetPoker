"""Document contenant la classe HUD_State qui va gérer l'affichage de chaque menu/page du jeu"""


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
from icecream import ic


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
        # Page par défaut dans le menu des paramètres
        self.setting_page = 1
        # Savoir si l'utilisateur paramètre le son
        self.is_setting_volume = False
        # Savoir si une table a été sélectionnée ou non (self.table_selected contient les infos de la table si oui, None si non)
        self.table_selected = None
        # Savoir si le code entré dans lobby est valide, et laisser afficher 2 secondes l'erreur
        self.error = [False, 0]
        # Savoir si on affiche un message de confirmation
        self.confirmation = False
        # Timer de début de la partie
        self.timer = [None, 0, False]
        self.round_started = False
        self.is_raising = False
        # Montant par défaut lorsque le joueur veut faire l'action "raise"
        self.raised_amount = 0
    
    def mainmenu(self):
        """mainmenu est la fonction qui fait tourner/afficher le menu principal
        """
        # Rassemblement de tout les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # On gére les raccourcis clavier
            elif event.type == pygame.KEYDOWN:
                if event.unicode in Global_objects.raccourcis_mainmenu.keys():
                    check_click(Global_objects.raccourcis_mainmenu[event.unicode])

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
            gui_font = pygame.font.SysFont("Roboto", width_scale(20, self.largeur_actuelle), False, True)
            text_surf = gui_font.render("Go to the official MWTE website", True, "#000000")
            pygame.draw.rect(self.screen, "#FFFFFF", pygame.Rect((width_scale(mouse_pos[0], self.largeur_actuelle), height_scale(mouse_pos[1] + 15, self.hauteur_actuelle)), (width_scale(210, self.largeur_actuelle), height_scale(20, self.hauteur_actuelle))), border_radius = 3)
            self.screen.blit(text_surf, (width_scale(mouse_pos[0], self.largeur_actuelle), height_scale(mouse_pos[1] + 20, self.hauteur_actuelle)))
            # On gére le cas où on clique sur le logo pour ouvrir UNE SEULE FOIS notre site web
            if pygame.mouse.get_pressed()[0]:
                self.is_pressing = True
            else:
                if self.is_pressing:
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
        # Cliquer sur le bouton SHOP affiche l'historique des parties
        Global_objects.shopbutton.draw()

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
            elif Global_objects.tablecodeinput.active:
                if event.type == pygame.KEYDOWN:
                    # Si on clique sur delete
                    if event.key == pygame.K_BACKSPACE:
                        Global_objects.tablecodeinput.backspace = True
                    # Si on clique sur entrer
                    elif event.key == pygame.K_RETURN:
                        # On essaie de rejoindre la partie avec le code entré
                        Global_objects.previewlobbys.players = None
                        try:
                            lobby_id = int(Global_objects.tablecodeinput.user_text)
                            Global_objects.previewlobbys.players = ask_sits_infos(Global_objects.client_socket,lobby_id)
                            time.sleep(0.1)
                            join_lobby(Global_objects.client_socket,lobby_id)
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
                            for lobby in Global_objects.displayed_lobbys_list:
                                if lobby[-1] == Global_objects.tablecodeinput.user_text:
                                    self.server_test = f"{lobby[0]}                                   {lobby[1]}                                   {lobby[2]}                                   {lobby[3]}                                   {lobby[4]}"
                                    Global_objects.pot = lobby[3]
                                    break
                            Global_objects.game_state.table_selected = None
                            Global_objects.game_state.back_pile = []
                            Global_objects.game_state.state = "Game Menu"
                            Global_objects.is_selecting_sit[0] = True
                            self.round_started = False
                            self.timer[1] = time.time()
                            Global_objects.parole = 1
                            # Temporaire pour afficher les cartes le temps que je recoive réellement des cartes
                            body = ["kh","1d"]
                            Global_objects.nombre_cartes = len(body)
                            try:
                                Global_objects.card_1 = body[0]
                                Global_objects.card_2 = body[1]
                            except:
                                pass
                        except:
                            self.error[0] = True
                            self.error[1] = time.time()
                        Global_objects.tablecodeinput.user_text = ""
                    # Si on clique sur n'importe quoi d'autre
                    else:
                        # On gère tout les cas de paramètres des objets de la classe TextInputBox (se référer au fichier TextInputBox_class.py pour plus d'informations sur ces paramètres)
                        if Global_objects.tablecodeinput.num_only:
                            if event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                if Global_objects.tablecodeinput.max_caracteres > 0:
                                    if len(Global_objects.tablecodeinput.user_text) < Global_objects.tablecodeinput.max_caracteres:
                                        if not Global_objects.tablecodeinput.adaptative_size:
                                            if Global_objects.tablecodeinput.text_size < Global_objects.tablecodeinput.base_size:
                                                Global_objects.tablecodeinput.user_text += event.unicode
                                        else:
                                            Global_objects.tablecodeinput.user_text += event.unicode
                        else:
                            if len(Global_objects.tablecodeinput.user_text) < Global_objects.tablecodeinput.max_caracteres or Global_objects.tablecodeinput.max_caracteres == -1:
                                if not Global_objects.tablecodeinput.adaptative_size:
                                    if Global_objects.tablecodeinput.text_size < Global_objects.tablecodeinput.base_size:
                                        Global_objects.tablecodeinput.user_text += event.unicode
                                    else:
                                        Global_objects.tablecodeinput.user_text += event.unicode
                                else:
                                    Global_objects.tablecodeinput.user_text += event.unicode
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        Global_objects.tablecodeinput.backspace = False
            # On gére les raccourcis clavier
            elif event.type == pygame.KEYDOWN:
                if event.unicode in Global_objects.raccourcis_lobbymenu.keys():
                    if event.unicode == list(Global_objects.raccourcis_lobbymenu.keys())[0]:
                        Global_objects.tablecodeinput.active = True
                    elif event.unicode == list(Global_objects.raccourcis_lobbymenu.keys())[1]:
                        if not self.table_selected is None:
                            check_click(Global_objects.raccourcis_lobbymenu[event.unicode])
                    else:
                        check_click(Global_objects.raccourcis_lobbymenu[event.unicode])
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Molette de la souris vers le haut
                if event.button == 4:
                    Global_objects.serverscrollbox.scroll_up()
                # Molette de la souris vers le bas    
                elif event.button == 5:
                    Global_objects.serverscrollbox.scroll_down()

        # Dessine l'image de fond sur la self.screen de l'écran
        self.screen.blit(self.fond, (0, 0))

        # Dessin de la scrollbox et des infos des colonnes de la scrollbox
        gui_font = pygame.font.SysFont("Roboto", width_scale(27, self.largeur_actuelle))
        text_surf = gui_font.render("Lobby name", True, "#FFFFFF")
        self.screen.blit(text_surf, (width_scale(225, self.largeur_actuelle), height_scale(210, self.hauteur_actuelle)))
        text_surf = gui_font.render("Number of players", True, "#FFFFFF")
        self.screen.blit(text_surf, (width_scale(370, self.largeur_actuelle), height_scale(210, self.hauteur_actuelle)))
        text_surf = gui_font.render("Bet amount", True, "#FFFFFF")
        self.screen.blit(text_surf, (width_scale(570, self.largeur_actuelle), height_scale(210, self.hauteur_actuelle)))
        text_surf = gui_font.render("Medium pot", True, "#FFFFFF")
        self.screen.blit(text_surf, (width_scale(740, self.largeur_actuelle), height_scale(210, self.hauteur_actuelle)))
        text_surf = gui_font.render("Medium rug", True, "#FFFFFF")
        self.screen.blit(text_surf, (width_scale(900, self.largeur_actuelle), height_scale(210, self.hauteur_actuelle)))
        text_surf = gui_font.render("ID of the table", True, "#FFFFFF")
        self.screen.blit(text_surf, (width_scale(1080, self.largeur_actuelle), height_scale(210, self.hauteur_actuelle)))
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
        # On gére le cas où l'utilisateur garde appuyé la touche backspace
        try:
            if Global_objects.tablecodeinput.backspace:
                if time.time() >= Global_objects.backspace_timer:
                    Global_objects.tablecodeinput.user_text = Global_objects.tablecodeinput.user_text[:-1]
                    Global_objects.backspace_timer = time.time() + 0.1
        except:
            pass
        # On affiche un texte au-dessus de la box qui indique ce que cette dernière fait
        gui_font = pygame.font.SysFont("Roboto", 50)
        text_surf = gui_font.render("Private Table Code", True, "#000000")
        self.screen.blit(text_surf, (width_scale(1370, self.largeur_actuelle), height_scale(850, self.hauteur_actuelle)))

        if not self.table_selected is None:
            # On crée la preview des tables
            try:
                Global_objects.previewlobbys.draw()
            except:
                pass
        
        if self.error[0]:
            # Affichage d'un message d'erreur dans le cas où le code de lobby n'existe pas
            gui_font = pygame.font.SysFont("Roboto", width_scale(70, self.largeur_actuelle))
            text_surf = gui_font.render("ERROR : NO GAME FOUND", True, "#FFFFFF")
            pygame.draw.rect(self.screen, "#FF0000", pygame.Rect((width_scale(650, self.largeur_actuelle), height_scale(400, self.hauteur_actuelle)), (width_scale(650, self.largeur_actuelle), height_scale(100, self.hauteur_actuelle))), border_radius = 2)
            self.screen.blit(text_surf, (width_scale(655, self.largeur_actuelle), height_scale(430, self.hauteur_actuelle)))
            # On vérifie si le message est là depuis plus de 1 secondes et dans ce cas on l'efface
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
            # Si on a sélectionne la raccourci_mainmenu_play
            if Global_objects.raccourci_mainmenu_play.active:
                if event.type == pygame.KEYDOWN:
                    # Si on clique sur supprimer
                    if event.key == pygame.K_BACKSPACE:
                        Global_objects.raccourci_mainmenu_play.user_text = "Backspace"
                        Global_objects.raccourci_mainmenu_play.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[0] = (event.unicode, dict_list[0][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur echap
                    elif event.key == pygame.K_ESCAPE:
                        Global_objects.raccourci_mainmenu_play.user_text = "Esc"
                        Global_objects.raccourci_mainmenu_play.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[0] = (event.unicode, dict_list[0][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur entrer
                    elif event.key == pygame.K_RETURN:
                        Global_objects.raccourci_mainmenu_play.user_text = "Enter"
                        Global_objects.raccourci_mainmenu_play.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[0] = (event.unicode, dict_list[0][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur tab
                    elif event.key == pygame.K_TAB:
                        Global_objects.raccourci_mainmenu_play.user_text = "Tab"
                        Global_objects.raccourci_mainmenu_play.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[0] = (event.unicode, dict_list[0][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur n'importe quoi d'autre
                    elif event.unicode != "":
                        # On gère tout les cas de paramètres des objets de la classe TextInputBox (se référer au fichier TextInputBox_class.py pour plus d'informations sur ces paramètres)
                        if Global_objects.raccourci_mainmenu_play.num_only:
                            if event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                if Global_objects.raccourci_mainmenu_play.max_caracteres > 0:
                                    if len(Global_objects.raccourci_mainmenu_play.user_text) < Global_objects.raccourci_mainmenu_play.max_caracteres:
                                        if not Global_objects.raccourci_mainmenu_play.adaptative_size:
                                            if Global_objects.raccourci_mainmenu_play.text_size < Global_objects.raccourci_mainmenu_play.base_size:
                                                Global_objects.raccourci_mainmenu_play.user_text = event.unicode
                                                Global_objects.raccourci_mainmenu_play.active = False
                                                dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                                dict_list[0] = (Global_objects.raccourci_mainmenu_play.user_text, dict_list[0][1])
                                                Global_objects.raccourcis_mainmenu = dict(dict_list)
                                        else:
                                            Global_objects.raccourci_mainmenu_play.user_text = event.unicode
                                            Global_objects.raccourci_mainmenu_play.active = False
                                            dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                            dict_list[0] = (Global_objects.raccourci_mainmenu_play.user_text, dict_list[0][1])
                                            Global_objects.raccourcis_mainmenu = dict(dict_list)
                        else:
                            if len(Global_objects.raccourci_mainmenu_play.user_text) < Global_objects.raccourci_mainmenu_play.max_caracteres or Global_objects.raccourci_mainmenu_play.max_caracteres == -1:
                                if not Global_objects.raccourci_mainmenu_play.adaptative_size:
                                    if Global_objects.raccourci_mainmenu_play.text_size < Global_objects.raccourci_mainmenu_play.base_size:
                                        Global_objects.raccourci_mainmenu_play.user_text = event.unicode
                                        Global_objects.raccourci_mainmenu_play.active = False
                                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                        dict_list[0] = (Global_objects.raccourci_mainmenu_play.user_text, dict_list[0][1])
                                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                                    else:
                                        Global_objects.raccourci_mainmenu_play.user_text = event.unicode
                                        Global_objects.raccourci_mainmenu_play.active = False
                                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                        dict_list[0] = (Global_objects.raccourci_mainmenu_play.user_text, dict_list[0][1])
                                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                                else:
                                    Global_objects.raccourci_mainmenu_play.user_text = event.unicode
                                    Global_objects.raccourci_mainmenu_play.active = False
                                    dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                    dict_list[0] = (Global_objects.raccourci_mainmenu_play.user_text, dict_list[0][1])
                                    Global_objects.raccourcis_mainmenu = dict(dict_list)
            # Si on a sélectionne la raccourci_mainmenu_settings
            if Global_objects.raccourci_mainmenu_settings.active:
                if event.type == pygame.KEYDOWN:
                    # Si on clique sur supprimer
                    if event.key == pygame.K_BACKSPACE:
                        Global_objects.raccourci_mainmenu_settings.user_text = "Backspace"
                        Global_objects.raccourci_mainmenu_settings.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[1] = (event.unicode, dict_list[1][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur echap
                    elif event.key == pygame.K_ESCAPE:
                        Global_objects.raccourci_mainmenu_settings.user_text = "Esc"
                        Global_objects.raccourci_mainmenu_settings.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[1] = (event.unicode, dict_list[1][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur entrer
                    elif event.key == pygame.K_RETURN:
                        Global_objects.raccourci_mainmenu_settings.user_text = "Enter"
                        Global_objects.raccourci_mainmenu_settings.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[1] = (event.unicode, dict_list[1][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur tab
                    elif event.key == pygame.K_TAB:
                        Global_objects.raccourci_mainmenu_settings.user_text = "Tab"
                        Global_objects.raccourci_mainmenu_settings.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[1] = (event.unicode, dict_list[1][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur n'importe quoi d'autre
                    elif event.unicode != "":
                        # On gère tout les cas de paramètres des objets de la classe TextInputBox (se référer au fichier TextInputBox_class.py pour plus d'informations sur ces paramètres)
                        if Global_objects.raccourci_mainmenu_settings.num_only:
                            if event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                if Global_objects.raccourci_mainmenu_settings.max_caracteres > 0:
                                    if len(Global_objects.raccourci_mainmenu_settings.user_text) < Global_objects.raccourci_mainmenu_settings.max_caracteres:
                                        if not Global_objects.raccourci_mainmenu_settings.adaptative_size:
                                            if Global_objects.raccourci_mainmenu_settings.text_size < Global_objects.raccourci_mainmenu_settings.base_size:
                                                Global_objects.raccourci_mainmenu_settings.user_text = event.unicode
                                                Global_objects.raccourci_mainmenu_settings.active = False
                                                dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                                dict_list[1] = (Global_objects.raccourci_mainmenu_settings.user_text, dict_list[1][1])
                                                Global_objects.raccourcis_mainmenu = dict(dict_list)
                                        else:
                                            Global_objects.raccourci_mainmenu_settings.user_text = event.unicode
                                            Global_objects.raccourci_mainmenu_settings.active = False
                                            dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                            dict_list[1] = (Global_objects.raccourci_mainmenu_settings.user_text, dict_list[1][1])
                                            Global_objects.raccourcis_mainmenu = dict(dict_list)
                        else:
                            if len(Global_objects.raccourci_mainmenu_settings.user_text) < Global_objects.raccourci_mainmenu_settings.max_caracteres or Global_objects.raccourci_mainmenu_settings.max_caracteres == -1:
                                if not Global_objects.raccourci_mainmenu_settings.adaptative_size:
                                    if Global_objects.raccourci_mainmenu_settings.text_size < Global_objects.raccourci_mainmenu_settings.base_size:
                                        Global_objects.raccourci_mainmenu_settings.user_text = event.unicode
                                        Global_objects.raccourci_mainmenu_settings.active = False
                                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                        dict_list[1] = (Global_objects.raccourci_mainmenu_settings.user_text, dict_list[1][1])
                                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                                    else:
                                        Global_objects.raccourci_mainmenu_settings.user_text = event.unicode
                                        Global_objects.raccourci_mainmenu_settings.active = False
                                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                        dict_list[1] = (Global_objects.raccourci_mainmenu_settings.user_text, dict_list[1][1])
                                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                                else:
                                    Global_objects.raccourci_mainmenu_settings.user_text = event.unicode
                                    Global_objects.raccourci_mainmenu_settings.active = False
                                    dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                    dict_list[1] = (Global_objects.raccourci_mainmenu_settings.user_text, dict_list[1][1])
                                    Global_objects.raccourcis_mainmenu = dict(dict_list)
            # Si on a sélectionne la raccourci_mainmenu_shop
            if Global_objects.raccourci_mainmenu_shop.active:
                if event.type == pygame.KEYDOWN:
                    # Si on clique sur supprimer
                    if event.key == pygame.K_BACKSPACE:
                        Global_objects.raccourci_mainmenu_shop.user_text = "Backspace"
                        Global_objects.raccourci_mainmenu_shop.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[2] = (event.unicode, dict_list[2][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur echap
                    elif event.key == pygame.K_ESCAPE:
                        Global_objects.raccourci_mainmenu_shop.user_text = "Esc"
                        Global_objects.raccourci_mainmenu_shop.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[2] = (event.unicode, dict_list[2][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur entrer
                    elif event.key == pygame.K_RETURN:
                        Global_objects.raccourci_mainmenu_shop.user_text = "Enter"
                        Global_objects.raccourci_mainmenu_shop.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[2] = (event.unicode, dict_list[2][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur tab
                    elif event.key == pygame.K_TAB:
                        Global_objects.raccourci_mainmenu_shop.user_text = "Tab"
                        Global_objects.raccourci_mainmenu_shop.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[2] = (event.unicode, dict_list[2][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur n'importe quoi d'autre
                    elif event.unicode != "":
                        # On gère tout les cas de paramètres des objets de la classe TextInputBox (se référer au fichier TextInputBox_class.py pour plus d'informations sur ces paramètres)
                        if Global_objects.raccourci_mainmenu_shop.num_only:
                            if event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                if Global_objects.raccourci_mainmenu_shop.max_caracteres > 0:
                                    if len(Global_objects.raccourci_mainmenu_shop.user_text) < Global_objects.raccourci_mainmenu_shop.max_caracteres:
                                        if not Global_objects.raccourci_mainmenu_shop.adaptative_size:
                                            if Global_objects.raccourci_mainmenu_shop.text_size < Global_objects.raccourci_mainmenu_shop.base_size:
                                                Global_objects.raccourci_mainmenu_shop.user_text = event.unicode
                                                Global_objects.raccourci_mainmenu_shop.active = False
                                                dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                                dict_list[2] = (Global_objects.raccourci_mainmenu_shop.user_text, dict_list[2][1])
                                                Global_objects.raccourcis_mainmenu = dict(dict_list)
                                        else:
                                            Global_objects.raccourci_mainmenu_shop.user_text = event.unicode
                                            Global_objects.raccourci_mainmenu_shop.active = False
                                            dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                            dict_list[2] = (Global_objects.raccourci_mainmenu_shop.user_text, dict_list[2][1])
                                            Global_objects.raccourcis_mainmenu = dict(dict_list)
                        else:
                            if len(Global_objects.raccourci_mainmenu_shop.user_text) < Global_objects.raccourci_mainmenu_shop.max_caracteres or Global_objects.raccourci_mainmenu_shop.max_caracteres == -1:
                                if not Global_objects.raccourci_mainmenu_shop.adaptative_size:
                                    if Global_objects.raccourci_mainmenu_shop.text_size < Global_objects.raccourci_mainmenu_shop.base_size:
                                        Global_objects.raccourci_mainmenu_shop.user_text = event.unicode
                                        Global_objects.raccourci_mainmenu_shop.active = False
                                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                        dict_list[2] = (Global_objects.raccourci_mainmenu_shop.user_text, dict_list[2][1])
                                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                                    else:
                                        Global_objects.raccourci_mainmenu_shop.user_text = event.unicode
                                        Global_objects.raccourci_mainmenu_shop.active = False
                                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                        dict_list[2] = (Global_objects.raccourci_mainmenu_shop.user_text, dict_list[2][1])
                                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                                else:
                                    Global_objects.raccourci_mainmenu_shop.user_text = event.unicode
                                    Global_objects.raccourci_mainmenu_shop.active = False
                                    dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                    dict_list[2] = (Global_objects.raccourci_mainmenu_shop.user_text, dict_list[2][1])
                                    Global_objects.raccourcis_mainmenu = dict(dict_list)
            # Si on a sélectionne la raccourci_mainmenu_account
            if Global_objects.raccourci_mainmenu_account.active:
                if event.type == pygame.KEYDOWN:
                    # Si on clique sur supprimer
                    if event.key == pygame.K_BACKSPACE:
                        Global_objects.raccourci_mainmenu_account.user_text = "Backspace"
                        Global_objects.raccourci_mainmenu_account.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[3] = (event.unicode, dict_list[3][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur echap
                    elif event.key == pygame.K_ESCAPE:
                        Global_objects.raccourci_mainmenu_account.user_text = "Esc"
                        Global_objects.raccourci_mainmenu_account.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[3] = (event.unicode, dict_list[3][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur entrer
                    elif event.key == pygame.K_RETURN:
                        Global_objects.raccourci_mainmenu_account.user_text = "Enter"
                        Global_objects.raccourci_mainmenu_account.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[3] = (event.unicode, dict_list[3][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur tab
                    elif event.key == pygame.K_TAB:
                        Global_objects.raccourci_mainmenu_account.user_text = "Tab"
                        Global_objects.raccourci_mainmenu_account.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[3] = (event.unicode, dict_list[3][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur n'importe quoi d'autre
                    elif event.unicode != "":
                        # On gère tout les cas de paramètres des objets de la classe TextInputBox (se référer au fichier TextInputBox_class.py pour plus d'informations sur ces paramètres)
                        if Global_objects.raccourci_mainmenu_account.num_only:
                            if event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                if Global_objects.raccourci_mainmenu_account.max_caracteres > 0:
                                    if len(Global_objects.raccourci_mainmenu_account.user_text) < Global_objects.raccourci_mainmenu_account.max_caracteres:
                                        if not Global_objects.raccourci_mainmenu_account.adaptative_size:
                                            if Global_objects.raccourci_mainmenu_account.text_size < Global_objects.raccourci_mainmenu_account.base_size:
                                                Global_objects.raccourci_mainmenu_account.user_text = event.unicode
                                                Global_objects.raccourci_mainmenu_account.active = False
                                                dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                                dict_list[3] = (Global_objects.raccourci_mainmenu_account.user_text, dict_list[3][1])
                                                Global_objects.raccourcis_mainmenu = dict(dict_list)
                                        else:
                                            Global_objects.raccourci_mainmenu_account.user_text = event.unicode
                                            Global_objects.raccourci_mainmenu_account.active = False
                                            dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                            dict_list[3] = (Global_objects.raccourci_mainmenu_account.user_text, dict_list[3][1])
                                            Global_objects.raccourcis_mainmenu = dict(dict_list)
                        else:
                            if len(Global_objects.raccourci_mainmenu_account.user_text) < Global_objects.raccourci_mainmenu_account.max_caracteres or Global_objects.raccourci_mainmenu_account.max_caracteres == -1:
                                if not Global_objects.raccourci_mainmenu_account.adaptative_size:
                                    if Global_objects.raccourci_mainmenu_account.text_size < Global_objects.raccourci_mainmenu_account.base_size:
                                        Global_objects.raccourci_mainmenu_account.user_text = event.unicode
                                        Global_objects.raccourci_mainmenu_account.active = False
                                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                        dict_list[3] = (Global_objects.raccourci_mainmenu_account.user_text, dict_list[3][1])
                                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                                    else:
                                        Global_objects.raccourci_mainmenu_account.user_text = event.unicode
                                        Global_objects.raccourci_mainmenu_account.active = False
                                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                        dict_list[3] = (Global_objects.raccourci_mainmenu_account.user_text, dict_list[3][1])
                                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                                else:
                                    Global_objects.raccourci_mainmenu_account.user_text = event.unicode
                                    Global_objects.raccourci_mainmenu_account.active = False
                                    dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                    dict_list[3] = (Global_objects.raccourci_mainmenu_account.user_text, dict_list[3][1])
                                    Global_objects.raccourcis_mainmenu = dict(dict_list)
            # Si on a sélectionne la raccourci_mainmenu_back
            if Global_objects.raccourci_mainmenu_back.active:
                if event.type == pygame.KEYDOWN:
                    # Si on clique sur supprimer
                    if event.key == pygame.K_BACKSPACE:
                        Global_objects.raccourci_mainmenu_back.user_text = "Backspace"
                        Global_objects.raccourci_mainmenu_back.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[4] = (event.unicode, dict_list[4][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur echap
                    elif event.key == pygame.K_ESCAPE:
                        Global_objects.raccourci_mainmenu_back.user_text = "Esc"
                        Global_objects.raccourci_mainmenu_back.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[4] = (event.unicode, dict_list[4][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur entrer
                    elif event.key == pygame.K_RETURN:
                        Global_objects.raccourci_mainmenu_back.user_text = "Enter"
                        Global_objects.raccourci_mainmenu_back.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[4] = (event.unicode, dict_list[4][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur tab
                    elif event.key == pygame.K_TAB:
                        Global_objects.raccourci_mainmenu_back.user_text = "Tab"
                        Global_objects.raccourci_mainmenu_back.active = False
                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                        dict_list[4] = (event.unicode, dict_list[4][1])
                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                    # Si on clique sur n'importe quoi d'autre
                    elif event.unicode != "":
                        # On gère tout les cas de paramètres des objets de la classe TextInputBox (se référer au fichier TextInputBox_class.py pour plus d'informations sur ces paramètres)
                        if Global_objects.raccourci_mainmenu_back.num_only:
                            if event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                if Global_objects.raccourci_mainmenu_back.max_caracteres > 0:
                                    if len(Global_objects.raccourci_mainmenu_back.user_text) < Global_objects.raccourci_mainmenu_back.max_caracteres:
                                        if not Global_objects.raccourci_mainmenu_back.adaptative_size:
                                            if Global_objects.raccourci_mainmenu_back.text_size < Global_objects.raccourci_mainmenu_back.base_size:
                                                Global_objects.raccourci_mainmenu_back.user_text = event.unicode
                                                Global_objects.raccourci_mainmenu_back.active = False
                                                dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                                dict_list[4] = (Global_objects.raccourci_mainmenu_back.user_text, dict_list[4][1])
                                                Global_objects.raccourcis_mainmenu = dict(dict_list)
                                        else:
                                            Global_objects.raccourci_mainmenu_back.user_text = event.unicode
                                            Global_objects.raccourci_mainmenu_back.active = False
                                            dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                            dict_list[4] = (Global_objects.raccourci_mainmenu_back.user_text, dict_list[4][1])
                                            Global_objects.raccourcis_mainmenu = dict(dict_list)
                        else:
                            if len(Global_objects.raccourci_mainmenu_back.user_text) < Global_objects.raccourci_mainmenu_back.max_caracteres or Global_objects.raccourci_mainmenu_back.max_caracteres == -1:
                                if not Global_objects.raccourci_mainmenu_back.adaptative_size:
                                    if Global_objects.raccourci_mainmenu_back.text_size < Global_objects.raccourci_mainmenu_back.base_size:
                                        Global_objects.raccourci_mainmenu_back.user_text = event.unicode
                                        Global_objects.raccourci_mainmenu_back.active = False
                                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                        dict_list[4] = (Global_objects.raccourci_mainmenu_back.user_text, dict_list[4][1])
                                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                                    else:
                                        Global_objects.raccourci_mainmenu_back.user_text = event.unicode
                                        Global_objects.raccourci_mainmenu_back.active = False
                                        dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                        dict_list[4] = (Global_objects.raccourci_mainmenu_back.user_text, dict_list[4][1])
                                        Global_objects.raccourcis_mainmenu = dict(dict_list)
                                else:
                                    Global_objects.raccourci_mainmenu_back.user_text = event.unicode
                                    Global_objects.raccourci_mainmenu_back.active = False
                                    dict_list = list(Global_objects.raccourcis_mainmenu.items())
                                    dict_list[4] = (Global_objects.raccourci_mainmenu_back.user_text, dict_list[4][1])
                                    Global_objects.raccourcis_mainmenu = dict(dict_list)
            # On gére les raccourcis clavier
            elif event.type == pygame.KEYDOWN:
                if event.unicode in Global_objects.raccourcis_settingmenu.keys():
                    check_click(Global_objects.raccourcis_settingmenu[event.unicode])

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
            pygame.draw.rect(self.screen, "#0000E0", pygame.Rect((width_scale(280, self.largeur_actuelle), height_scale(180, self.hauteur_actuelle)), (width_scale(450, self.largeur_actuelle), height_scale(50, self.hauteur_actuelle))), border_radius = 3)
            gui_font = pygame.font.SysFont("Roboto", width_scale(50, self.largeur_actuelle))
            text_surf = gui_font.render("Volume", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(190, self.hauteur_actuelle)))
            # On affiche la barre de son
            if round(Global_objects.volume_music * 100) == 100:
                text_size = 20
            else:
                text_size = 25
            Global_objects.sound_bar.draw(round(Global_objects.volume_music * 100), width_scale(text_size, self.largeur_actuelle), width_scale(12, self.largeur_actuelle), height_scale(1, self.hauteur_actuelle))
            # On gére l'affichage avec les icônes de son
            if Global_objects.sound_bar.cursor_width <= Global_objects.sound_bar.x: # Barre à 0
                volume_icon = self.screen.blit(self.sounds_icons[0], (width_scale(415, self.largeur_actuelle), height_scale(172, self.hauteur_actuelle)))
            elif Global_objects.sound_bar.cursor_width > Global_objects.sound_bar.x and Global_objects.sound_bar.cursor_width <= Global_objects.sound_bar.width//3 + Global_objects.sound_bar.x: # Barre à 1/3
                volume_icon = self.screen.blit(self.sounds_icons[1], (width_scale(415, self.largeur_actuelle), height_scale(172, self.hauteur_actuelle)))
            elif Global_objects.sound_bar.cursor_width > Global_objects.sound_bar.width//3 + Global_objects.sound_bar.x and Global_objects.sound_bar.cursor_width <= (Global_objects.sound_bar.width//3)*2 + Global_objects.sound_bar.x: # Barre à 2/3
                volume_icon = self.screen.blit(self.sounds_icons[2], (width_scale(415, self.largeur_actuelle), height_scale(172, self.hauteur_actuelle)))
            elif Global_objects.sound_bar.cursor_width > (Global_objects.sound_bar.width//3)*2 + Global_objects.sound_bar.x: # Barre au dessus de 2/3
                volume_icon = self.screen.blit(self.sounds_icons[3], (width_scale(415, self.largeur_actuelle), height_scale(172, self.hauteur_actuelle)))
            # On gére l'utilisation/les interactions avec le bouton de son
            if not self.is_setting_volume:
                if volume_icon.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:
                        self.is_pressing = True
                    else:
                        if self.is_pressing:
                            if self.sound_on:
                                self.last_sound = Global_objects.sound_bar.cursor_width
                                Global_objects.sound_bar.cursor_width = Global_objects.sound_bar.x
                                self.sound_on = False
                            elif not self.sound_on:
                                Global_objects.sound_bar.cursor_width = self.last_sound
                                self.sound_on = True
                            self.is_pressing = False
                else:
                    self.is_pressing = False
            if Global_objects.sound_bar.cursor_width <= Global_objects.sound_bar.x:
                self.sound_on = False
            else:
                self.sound_on = True
            # On récupère le volume actuel
            Global_objects.volume_music = (Global_objects.sound_bar.cursor_width - width_scale(500, self.largeur_actuelle)) / (width_scale(700, self.largeur_actuelle) - width_scale(500, self.largeur_actuelle))
        # Page 2
        elif self.setting_page == 2:
            # Temporaire
            gui_font = pygame.font.SysFont("Roboto", 40)
            settingtext_surf = gui_font.render("2nd setting's page", True, "#FFFFFF")
            self.screen.blit(settingtext_surf, (width_scale(270, self.largeur_actuelle), height_scale(170, self.hauteur_actuelle)))
        # Page 3
        elif self.setting_page == 3:
            gui_font = pygame.font.SysFont("Roboto", 30)
            settingtext_surf = gui_font.render("Les touches prises en compte sont les touches à caractères ainsi que tab, esc, entrer et backspace. Les touches comme maj, ctrl ou alt par exemple ne sont pas prises en charge.", True, "#0000E0")
            self.screen.blit(settingtext_surf, (width_scale(10, self.largeur_actuelle), height_scale(1030, self.hauteur_actuelle)))
            # Raccourcis clavier
            # ZONE 1
            pygame.draw.rect(self.screen, "#0000E0", pygame.Rect((width_scale(280, self.largeur_actuelle), height_scale(180, self.hauteur_actuelle)), (width_scale(310, self.largeur_actuelle), height_scale(40, self.hauteur_actuelle))), border_radius = 3)
            gui_font = pygame.font.SysFont("Roboto", width_scale(40, self.largeur_actuelle))
            text_surf = gui_font.render("Main Menu Shortcuts", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(187, self.hauteur_actuelle)))
            pygame.draw.rect(self.screen, "#0000E0", pygame.Rect((width_scale(280, self.largeur_actuelle), height_scale(235, self.hauteur_actuelle)), (width_scale(700, self.largeur_actuelle), height_scale(205, self.hauteur_actuelle))), border_radius = 3)
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Play button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(245, self.hauteur_actuelle)))
            Global_objects.raccourci_mainmenu_play.draw()
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Settings button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(285, self.hauteur_actuelle)))
            Global_objects.raccourci_mainmenu_settings.draw()
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Shop button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(325, self.hauteur_actuelle)))
            Global_objects.raccourci_mainmenu_shop.draw()
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Account button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(365, self.hauteur_actuelle)))
            Global_objects.raccourci_mainmenu_account.draw()
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Exit button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(405, self.hauteur_actuelle)))
            Global_objects.raccourci_mainmenu_back.draw()

            # ZONE 2
            pygame.draw.rect(self.screen, "#0000E0", pygame.Rect((width_scale(280, self.largeur_actuelle), height_scale(455, self.hauteur_actuelle)), (width_scale(360, self.largeur_actuelle), height_scale(40, self.hauteur_actuelle))), border_radius = 3)
            gui_font = pygame.font.SysFont("Roboto", width_scale(40, self.largeur_actuelle))
            text_surf = gui_font.render("Settings Menu Shortcuts", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(462, self.hauteur_actuelle)))
            pygame.draw.rect(self.screen, "#0000E0", pygame.Rect((width_scale(280, self.largeur_actuelle), height_scale(510, self.hauteur_actuelle)), (width_scale(700, self.largeur_actuelle), height_scale(205, self.hauteur_actuelle))), border_radius = 3)
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Page 1 :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(520, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Page 2 :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(560, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Page 3 :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(600, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Account button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(640, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Back button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(680, self.hauteur_actuelle)))

            # ZONE 3
            pygame.draw.rect(self.screen, "#0000E0", pygame.Rect((width_scale(280, self.largeur_actuelle), height_scale(730, self.hauteur_actuelle)), (width_scale(360, self.largeur_actuelle), height_scale(40, self.hauteur_actuelle))), border_radius = 3)
            gui_font = pygame.font.SysFont("Roboto", width_scale(40, self.largeur_actuelle))
            text_surf = gui_font.render("Account Menu Shortcuts", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(737, self.hauteur_actuelle)))
            pygame.draw.rect(self.screen, "#0000E0", pygame.Rect((width_scale(280, self.largeur_actuelle), height_scale(785, self.hauteur_actuelle)), (width_scale(700, self.largeur_actuelle), height_scale(205, self.hauteur_actuelle))), border_radius = 3)
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Settings button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(795, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Pseudo input zone :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(835, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Bio input zone :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(875, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Deconnexion button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(915, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Back button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(955, self.hauteur_actuelle)))

            # ZONE 4
            pygame.draw.rect(self.screen, "#0000E0", pygame.Rect((width_scale(1030, self.largeur_actuelle), height_scale(180, self.hauteur_actuelle)), (width_scale(310, self.largeur_actuelle), height_scale(40, self.hauteur_actuelle))), border_radius = 3)
            gui_font = pygame.font.SysFont("Roboto", width_scale(40, self.largeur_actuelle))
            text_surf = gui_font.render("Ingame Shortcuts", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(187, self.hauteur_actuelle)))
            pygame.draw.rect(self.screen, "#0000E0", pygame.Rect((width_scale(1030, self.largeur_actuelle), height_scale(235, self.hauteur_actuelle)), (width_scale(700, self.largeur_actuelle), height_scale(480, self.hauteur_actuelle))), border_radius = 3)
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Check button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(245, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Call button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(285, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Fold button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(325, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Raise button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(365, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Yes/Confirm button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(405, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("No/Cancel button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(445, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("-100 button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(485, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("+100 button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(525, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("All in button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(565, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Sit up button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(605, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Leave game button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(645, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Settings button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(685, self.hauteur_actuelle)))

            # ZONE 5
            pygame.draw.rect(self.screen, "#0000E0", pygame.Rect((width_scale(1030, self.largeur_actuelle), height_scale(730, self.hauteur_actuelle)), (width_scale(360, self.largeur_actuelle), height_scale(40, self.hauteur_actuelle))), border_radius = 3)
            gui_font = pygame.font.SysFont("Roboto", width_scale(40, self.largeur_actuelle))
            text_surf = gui_font.render("Lobby Menu Shortcuts", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(737, self.hauteur_actuelle)))
            pygame.draw.rect(self.screen, "#0000E0", pygame.Rect((width_scale(1030, self.largeur_actuelle), height_scale(785, self.hauteur_actuelle)), (width_scale(700, self.largeur_actuelle), height_scale(205, self.hauteur_actuelle))), border_radius = 3)
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Join table button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(795, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Create table button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(835, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Table code input zone :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(875, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Account button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(915, self.hauteur_actuelle)))
            # Zone d'input pour changer le caractère
            gui_font = pygame.font.SysFont("Roboto", width_scale(35, self.largeur_actuelle))
            text_surf = gui_font.render("Back button :", True, "#FFFFFF")
            self.screen.blit(text_surf, (width_scale(1040, self.largeur_actuelle), height_scale(955, self.hauteur_actuelle)))

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
            if Global_objects.accountpseudoinput.active:
                if event.type == pygame.KEYDOWN:
                    # Si on clique sur supprimer
                    if event.key == pygame.K_BACKSPACE:
                        Global_objects.accountpseudoinput.backspace = True
                    # Si on clique sur entrer
                    elif event.key == pygame.K_RETURN:
                        Global_objects.accountpseudoinput.active = False
                    # Si on clique sur n'importe quoi d'autre
                    else:
                        # On gère tout les cas de paramètres des objets de la classe TextInputBox (se référer au fichier TextInputBox_class.py pour plus d'informations sur ces paramètres)
                        if Global_objects.accountpseudoinput.num_only:
                            if event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                if Global_objects.accountpseudoinput.max_caracteres > 0:
                                    if len(Global_objects.accountpseudoinput.user_text) < Global_objects.accountpseudoinput.max_caracteres:
                                        if not Global_objects.accountpseudoinput.adaptative_size:
                                            if Global_objects.accountpseudoinput.text_size < Global_objects.accountpseudoinput.base_size:
                                                Global_objects.accountpseudoinput.user_text += event.unicode
                                        else:
                                            Global_objects.accountpseudoinput.user_text += event.unicode
                        else:
                            if len(Global_objects.accountpseudoinput.user_text) < Global_objects.accountpseudoinput.max_caracteres or Global_objects.accountpseudoinput.max_caracteres == -1:
                                if not Global_objects.accountpseudoinput.adaptative_size:
                                    if Global_objects.accountpseudoinput.text_size < Global_objects.accountpseudoinput.base_size:
                                        Global_objects.accountpseudoinput.user_text += event.unicode
                                    else:
                                        Global_objects.accountpseudoinput.user_text += event.unicode
                                else:
                                    Global_objects.accountpseudoinput.user_text += event.unicode
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        Global_objects.accountpseudoinput.backspace = False
            # Si on a sélectionne la accountinformationinput
            elif Global_objects.accountinformationinput.active:
                if event.type == pygame.KEYDOWN:
                    # Si on clique sur delete
                    if event.key == pygame.K_BACKSPACE:
                        Global_objects.accountinformationinput.backspace = True
                    # Si on clique sur entrer
                    elif event.key == pygame.K_RETURN:
                        Global_objects.accountinformationinput.active = False
                    # Si on clique sur n'importe quoi d'autre
                    else:
                        # On gère tout les cas de paramètres des objets de la classe TextInputBox (se référer au fichier TextInputBox_class.py pour plus d'informations sur ces paramètres)
                        if Global_objects.accountinformationinput.num_only:
                            if event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                if Global_objects.accountinformationinput.max_caracteres > 0:
                                    if len(Global_objects.accountinformationinput.user_text) < Global_objects.accountinformationinput.max_caracteres:
                                        if not Global_objects.accountinformationinput.adaptative_size:
                                            if Global_objects.accountinformationinput.text_size < Global_objects.accountinformationinput.base_size:
                                                Global_objects.accountinformationinput.user_text += event.unicode
                                        else:
                                            Global_objects.accountinformationinput.user_text += event.unicode
                        else:
                            if len(Global_objects.accountinformationinput.user_text) < Global_objects.accountinformationinput.max_caracteres or Global_objects.accountinformationinput.max_caracteres == -1:
                                if not Global_objects.accountinformationinput.adaptative_size:
                                    if Global_objects.accountinformationinput.text_size < Global_objects.accountinformationinput.base_size:
                                        Global_objects.accountinformationinput.user_text += event.unicode
                                    else:
                                        Global_objects.accountinformationinput.user_text += event.unicode
                                else:
                                    Global_objects.accountinformationinput.user_text += event.unicode
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        Global_objects.accountinformationinput.backspace = False
            # On gére les raccourcis clavier
            elif event.type == pygame.KEYDOWN:
                if event.unicode in Global_objects.raccourcis_accountmenu.keys():
                    if event.unicode == list(Global_objects.raccourcis_accountmenu.keys())[0] and Global_objects.accountsettingsbutton.account_modifiable:
                        Global_objects.accountpseudoinput.active = True
                    elif event.unicode == list(Global_objects.raccourcis_accountmenu.keys())[1] and Global_objects.accountsettingsbutton.account_modifiable:
                        Global_objects.accountinformationinput.active = True
                    else:
                        check_click(Global_objects.raccourcis_accountmenu[event.unicode])

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
        # Affichage du bouton de déconnexion de l'utilisateur
        Global_objects.deconnexionbutton.draw()
        # Affichage du bouton de paramètres du compte de l'utilisateur
        Global_objects.accountsettingsbutton.draw()
        # Affichage du pseudo de l'utilisateur
        Global_objects.accountpseudoinput.draw()
        # On gére le cas où l'utilisateur garde appuyé la touche backspace
        try:
            if Global_objects.accountpseudoinput.backspace:
                if time.time() >= Global_objects.backspace_timer:
                    Global_objects.accountpseudoinput.user_text = Global_objects.accountpseudoinput.user_text[:-1]
                    Global_objects.backspace_timer = time.time() + 0.1
        except:
            pass
        # Affichage des infos de l'utilisateur
        Global_objects.accountinformationinput.draw()
        # On gére le cas où l'utilisateur garde appuyé la touche backspace
        try:
            if Global_objects.accountinformationinput.backspace:
                if time.time() >= Global_objects.backspace_timer:
                    Global_objects.accountinformationinput.user_text = Global_objects.accountinformationinput.user_text[:-1]
                    Global_objects.backspace_timer = time.time() + 0.1
        except:
            pass

        # Met à jour l'affichage de l'interface
        pygame.display.update()

    def shopmenu(self):
        """shopmenu est la fonction qui fait tourner/afficher le shop du jeu
        """
        # Rassemblement de tout les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Dessine l'image de fond sur la self.screen de l'écran (IMPORANT CAR SE SUPERPOSE A L'INTERFACE PRECEDENT ET PERMET DE "L'EFFACER")
        self.screen.blit(self.fond, (0, 0))

        # Affichage des infos de la table sélectionnée en placeholder
        gui_font = pygame.font.SysFont("Roboto", width_scale(40, self.largeur_actuelle))
        text_surf = gui_font.render("PAGE EN CONSTRUCTION : CETTE PAGE ACCUEILLERA UN SHOP PERMETTANT AUX JOUEURS D'ACHETER DES COSMETIQUES", True, "#FFFFFF")
        self.screen.blit(text_surf, (width_scale(100, self.largeur_actuelle), height_scale(510, self.hauteur_actuelle)))

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
        
        # Affichage des infos de la table sélectionnée en placeholder
        gui_font = pygame.font.SysFont("Roboto", width_scale(40, self.largeur_actuelle))
        text_surf = gui_font.render("PAGE EN CONSTRUCTION : CETTE PAGE ACCUEILLERA DES OPTIONS A SELECTIONNER AVANT DE CREER UNE PARTIE", True, "#FFFFFF")
        self.screen.blit(text_surf, (width_scale(100, self.largeur_actuelle), height_scale(510, self.hauteur_actuelle)))

        # Met à jour l'affichage de l'interface
        pygame.display.update()

    def gamemenu(self):
        """gamemenu est la fonction qui fait tourner/afficher l'interface en jeu
        """
        # Rassemblement de tout les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Si on a sélectionne la raiseamountinput
            if Global_objects.raiseamountinput.active:
                if event.type == pygame.KEYDOWN:
                    # Si on clique sur supprimer
                    if event.key == pygame.K_BACKSPACE:
                        Global_objects.raiseamountinput.backspace = True
                    # Si on clique sur entrer
                    elif event.key == pygame.K_RETURN:
                        nouvelle_valeur = int(Global_objects.raiseamountinput.user_text) if int(Global_objects.raiseamountinput.user_text) <= Global_objects.connected_account[2] and int(Global_objects.raiseamountinput.user_text) >= 0 else (((Global_objects.connected_account[2]/100)*Global_objects.game_state.raised_amount)*100)
                        Global_objects.raise_bar.cursor_width = width_scale(400, self.largeur_actuelle) + (nouvelle_valeur / Global_objects.connected_account[2]) * (width_scale(1530, self.largeur_actuelle) - width_scale(400, self.largeur_actuelle))
                        Global_objects.raiseamountinput.user_text = ""
                        Global_objects.raiseamountinput.active = False
                    # Si on clique sur n'importe quoi d'autre
                    else:
                        # On gère tout les cas de paramètres des objets de la classe TextInputBox (se référer au fichier TextInputBox_class.py pour plus d'informations sur ces paramètres)
                        if Global_objects.raiseamountinput.num_only:
                            if event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                                if Global_objects.raiseamountinput.max_caracteres > 0:
                                    if len(Global_objects.raiseamountinput.user_text) < Global_objects.raiseamountinput.max_caracteres:
                                        if not Global_objects.raiseamountinput.adaptative_size:
                                            if Global_objects.raiseamountinput.text_size < Global_objects.raiseamountinput.base_size:
                                                Global_objects.raiseamountinput.user_text += event.unicode
                                        else:
                                            Global_objects.raiseamountinput.user_text += event.unicode
                        else:
                            if len(Global_objects.raiseamountinput.user_text) < Global_objects.raiseamountinput.max_caracteres or Global_objects.raiseamountinput.max_caracteres == -1:
                                if not Global_objects.raiseamountinput.adaptative_size:
                                    if Global_objects.raiseamountinput.text_size < Global_objects.raiseamountinput.base_size:
                                        Global_objects.raiseamountinput.user_text += event.unicode
                                    else:
                                        Global_objects.raiseamountinput.user_text += event.unicode
                                else:
                                    Global_objects.raiseamountinput.user_text += event.unicode
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        Global_objects.raiseamountinput.backspace = False
            # On gére les raccourcis clavier
            elif event.type == pygame.KEYDOWN:
                if event.unicode in Global_objects.raccourcis_gamemenu.keys():
                    if event.unicode in list(Global_objects.raccourcis_gamemenu.keys())[:4]:
                        if Global_objects.parole == Global_objects.client_actuel:
                            check_click(Global_objects.raccourcis_gamemenu[event.unicode])
                    elif event.unicode in list(Global_objects.raccourcis_gamemenu.keys())[4]:
                        if self.is_raising:
                            check_click(Global_objects.raccourcis_gamemenu[event.unicode][1])
                        elif self.confirmation:
                            check_click(Global_objects.raccourcis_gamemenu[event.unicode][0])
                    elif event.unicode in list(Global_objects.raccourcis_gamemenu.keys())[5]:
                        if self.is_raising:
                            check_click(Global_objects.raccourcis_gamemenu[event.unicode][1])
                        elif self.confirmation:
                            check_click(Global_objects.raccourcis_gamemenu[event.unicode][0])
                    elif event.unicode in list(Global_objects.raccourcis_gamemenu.keys())[6:9]:
                        if self.is_raising:
                            check_click(Global_objects.raccourcis_gamemenu[event.unicode])
                    elif event.unicode in list(Global_objects.raccourcis_gamemenu.keys())[9]:
                        if not self.round_started:
                            check_click(Global_objects.raccourcis_gamemenu[event.unicode])
                    else:
                        check_click(Global_objects.raccourcis_gamemenu[event.unicode])

        # Fond noir
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect((0, 0), (self.largeur_actuelle, self.hauteur_actuelle)))
        # Dessine l'image de fond sur la self.screen de l'écran (IMPORANT CAR SE SUPERPOSE A L'INTERFACE PRECEDENT ET PERMET DE "L'EFFACER")
        table_fond = pygame.transform.scale(self.table_fond, (self.largeur_actuelle, height_scale(980, self.hauteur_actuelle)))
        self.screen.blit(table_fond, (0, 0))

        # Affichage des infos de la table sélectionnée en placeholder
        gui_font = pygame.font.SysFont("Roboto", width_scale(40, self.largeur_actuelle))
        text_surf = gui_font.render(self.server_test, True, "#FFFFFF")
        self.screen.blit(text_surf, (width_scale(250, self.largeur_actuelle), height_scale(100, self.hauteur_actuelle)))

        if not self.round_started and self.timer[2]:
        # Affichage du timer avant que la partie commence
            if self.timer[0] > 0:
                # On ne peut se lever que si la partie n'est pas encore commencée
                gui_font = pygame.font.SysFont("Roboto", width_scale(60, self.largeur_actuelle))
                if self.timer[0] > 5:
                    text_surf = gui_font.render(f"{round(self.timer[0])}", True, "#FFFFFF")
                else:
                    text_surf = gui_font.render(f"{round(self.timer[0], 1)}", True, "#FFFFFF")
                text_rect = text_surf.get_rect(center = (self.largeur_actuelle//2 - width_scale(100, self.largeur_actuelle), height_scale(30, self.hauteur_actuelle)))
                self.screen.blit(text_surf, text_rect)
                self.timer[0] = 20 - (time.time() - self.timer[1])
            elif self.timer[0] <= 0:
                self.round_started = True
                self.timer = [20, time.time(), False]
        # Affichage du nombre de joueurs présents sur le nombre de joueurs max
        if not self.round_started:
            Global_objects.sit_upbutton.draw()
            try:
                gui_font = pygame.font.SysFont("Roboto", width_scale(60, self.largeur_actuelle))
                players = 0
                if Global_objects.auto_arrived_sits is None:
                    text_surf = gui_font.render(f"0/{len(Global_objects.previewlobbys.players)}", True, "#FFFFFF")
                else:
                    for player in Global_objects.auto_arrived_sits:
                        if player[1] is not None:
                            players += 1
                    text_surf = gui_font.render(f"{players}/{len(Global_objects.auto_arrived_sits)}", True, "#FFFFFF")
                text_rect = text_surf.get_rect(center = (self.largeur_actuelle//2 + width_scale(100, self.largeur_actuelle), height_scale(30, self.hauteur_actuelle)))
                self.screen.blit(text_surf, text_rect)
            except:
                pass
        
        # Affichage du texte POT au dessus de la zone du pot
        gui_font = pygame.font.SysFont("Roboto", width_scale(45, self.largeur_actuelle))
        text_surf = gui_font.render(f"POT", True, "#FFFFFF")
        self.screen.blit(text_surf, (width_scale(935, self.largeur_actuelle), height_scale(445, self.hauteur_actuelle)))
        # Affichage de la zone du pot de la partie
        pot_surface = pygame.Surface((width_scale(50, self.largeur_actuelle), height_scale(50, self.hauteur_actuelle)), pygame.SRCALPHA)
        pygame.draw.circle(self.screen, (0, 0, 0, 128), (width_scale(965, self.largeur_actuelle), height_scale(515, self.hauteur_actuelle)), width_scale(35, self.largeur_actuelle))
        pot_surface = self.screen.blit(pot_surface, (width_scale(940, self.largeur_actuelle), height_scale(490, self.hauteur_actuelle)))
        # On place la valeur du pot au milieu de la zone
        gui_font = pygame.font.SysFont("Roboto", width_scale(30, self.largeur_actuelle))
        pot_texte = ""
        for caract in Global_objects.pot:
            if caract.lower() == "k":
                pot_texte += "000"
            else:
                pot_texte += caract
        text_surf = gui_font.render(f"{pot_texte}", True, "#FFFFFF")
        text_rect = text_surf.get_rect(center = (pot_surface.centerx, pot_surface.centery))
        self.screen.blit(text_surf, text_rect)

        # Boucle pour calculer le timer de chaque joueur pour prendre une décision 
        if self.round_started:
            if self.timer[0] > 0:
                self.timer[0] = 15 - (time.time() - self.timer[1])
            elif self.timer[0] <= 0:
                Global_objects.parole += 1
                if Global_objects.parole > len(Global_objects.previewlobbys.players):
                    Global_objects.parole = 1
                self.timer = [15, time.time(), False]

        # Affichage de la zone qui comportera les actions du joueur
        # Boutons d'actions
        # On rend les boutons interagissables en fonction de si le siège sur lequel le joueur est assis et le siège qui posséde la parole ou non
        if Global_objects.parole == Global_objects.client_actuel and self.round_started:
            Global_objects.checkbutton.button_interactible = True
            Global_objects.callbutton.button_interactible = True
            Global_objects.foldbutton.button_interactible = True
            Global_objects.raisebutton.button_interactible = True
        else:
            Global_objects.checkbutton.button_interactible = False
            Global_objects.callbutton.button_interactible = False
            Global_objects.foldbutton.button_interactible = False
            Global_objects.raisebutton.button_interactible = False
        # On dessine les boutons
        Global_objects.checkbutton.draw()
        Global_objects.callbutton.draw()
        Global_objects.foldbutton.draw()
        Global_objects.raisebutton.draw()

        # Attribution des infos des sièges
        try:
            Global_objects.sit_1.player = Global_objects.auto_arrived_sits[0]
            Global_objects.sit_2.player = Global_objects.auto_arrived_sits[1]
            Global_objects.sit_3.player = Global_objects.auto_arrived_sits[2]
            Global_objects.sit_4.player = Global_objects.auto_arrived_sits[3]
            Global_objects.sit_5.player = Global_objects.auto_arrived_sits[4]
            Global_objects.sit_6.player = Global_objects.auto_arrived_sits[5]
            Global_objects.sit_7.player = Global_objects.auto_arrived_sits[6]
            Global_objects.sit_8.player = Global_objects.auto_arrived_sits[7]
            Global_objects.sit_9.player = Global_objects.auto_arrived_sits[8]
            Global_objects.sit_10.player = Global_objects.auto_arrived_sits[9]
        except:
            pass

        # Affichage des sièges en fonction du pattern suivant
        match len(Global_objects.previewlobbys.players):

            case 2:
                Global_objects.sit_1.x = width_scale(450, self.largeur_actuelle)
                Global_objects.sit_1.y = height_scale(450, self.hauteur_actuelle)
                Global_objects.sit_1.draw()
                Global_objects.sit_2.x = width_scale(1230, self.largeur_actuelle)
                Global_objects.sit_2.y = height_scale(450, self.hauteur_actuelle)
                Global_objects.sit_2.draw()

            case 3:
                Global_objects.sit_1.x = width_scale(840, self.largeur_actuelle)
                Global_objects.sit_1.y = height_scale(200, self.hauteur_actuelle)
                Global_objects.sit_1.draw()
                Global_objects.sit_2.x = width_scale(500, self.largeur_actuelle)
                Global_objects.sit_2.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_2.draw()
                Global_objects.sit_3.x = width_scale(1180, self.largeur_actuelle)
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
                Global_objects.sit_2.y = height_scale(440, self.hauteur_actuelle)
                Global_objects.sit_2.draw()
                Global_objects.sit_3.x = width_scale(1080, self.largeur_actuelle)
                Global_objects.sit_3.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_3.draw()
                Global_objects.sit_4.x = width_scale(600, self.largeur_actuelle)
                Global_objects.sit_4.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_4.draw()
                Global_objects.sit_5.x = width_scale(380, self.largeur_actuelle)
                Global_objects.sit_5.y = height_scale(440, self.hauteur_actuelle)
                Global_objects.sit_5.draw()

            case 6:
                Global_objects.sit_1.x = width_scale(540, self.largeur_actuelle)
                Global_objects.sit_1.y = height_scale(200, self.hauteur_actuelle)
                Global_objects.sit_1.draw()
                Global_objects.sit_2.x = width_scale(1140, self.largeur_actuelle)
                Global_objects.sit_2.y = height_scale(200, self.hauteur_actuelle)
                Global_objects.sit_2.draw()
                Global_objects.sit_3.x = width_scale(1360, self.largeur_actuelle)
                Global_objects.sit_3.y = height_scale(450, self.hauteur_actuelle)
                Global_objects.sit_3.draw()
                Global_objects.sit_4.x = width_scale(1140, self.largeur_actuelle)
                Global_objects.sit_4.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_4.draw()
                Global_objects.sit_5.x = width_scale(520, self.largeur_actuelle)
                Global_objects.sit_5.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_5.draw()
                Global_objects.sit_6.x = width_scale(340, self.largeur_actuelle)
                Global_objects.sit_6.y = height_scale(450, self.hauteur_actuelle)
                Global_objects.sit_6.draw()

            case 7:
                Global_objects.sit_1.x = width_scale(840, self.largeur_actuelle)
                Global_objects.sit_1.y = height_scale(200, self.hauteur_actuelle)
                Global_objects.sit_1.draw()
                Global_objects.sit_2.x = width_scale(1360, self.largeur_actuelle)
                Global_objects.sit_2.y = height_scale(350, self.hauteur_actuelle)
                Global_objects.sit_2.draw()
                Global_objects.sit_3.x = width_scale(1360, self.largeur_actuelle)
                Global_objects.sit_3.y = height_scale(550, self.hauteur_actuelle)
                Global_objects.sit_3.draw()
                Global_objects.sit_4.x = width_scale(1040, self.largeur_actuelle)
                Global_objects.sit_4.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_4.draw()
                Global_objects.sit_5.x = width_scale(650, self.largeur_actuelle)
                Global_objects.sit_5.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_5.draw()
                Global_objects.sit_6.x = width_scale(320, self.largeur_actuelle)
                Global_objects.sit_6.y = height_scale(550, self.hauteur_actuelle)
                Global_objects.sit_6.draw()
                Global_objects.sit_7.x = width_scale(320, self.largeur_actuelle)
                Global_objects.sit_7.y = height_scale(350, self.hauteur_actuelle)
                Global_objects.sit_7.draw()

            case 8:
                Global_objects.sit_1.x = width_scale(650, self.largeur_actuelle)
                Global_objects.sit_1.y = height_scale(200, self.hauteur_actuelle)
                Global_objects.sit_1.draw()
                Global_objects.sit_2.x = width_scale(1040, self.largeur_actuelle)
                Global_objects.sit_2.y = height_scale(200, self.hauteur_actuelle)
                Global_objects.sit_2.draw()
                Global_objects.sit_3.x = width_scale(1360, self.largeur_actuelle)
                Global_objects.sit_3.y = height_scale(350, self.hauteur_actuelle)
                Global_objects.sit_3.draw()
                Global_objects.sit_4.x = width_scale(1360, self.largeur_actuelle)
                Global_objects.sit_4.y = height_scale(550, self.hauteur_actuelle)
                Global_objects.sit_4.draw()
                Global_objects.sit_5.x = width_scale(1040, self.largeur_actuelle)
                Global_objects.sit_5.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_5.draw()
                Global_objects.sit_6.x = width_scale(650, self.largeur_actuelle)
                Global_objects.sit_6.y = height_scale(700, self.hauteur_actuelle)
                Global_objects.sit_6.draw()
                Global_objects.sit_7.x = width_scale(320, self.largeur_actuelle)
                Global_objects.sit_7.y = height_scale(550, self.hauteur_actuelle)
                Global_objects.sit_7.draw()
                Global_objects.sit_8.x = width_scale(320, self.largeur_actuelle)
                Global_objects.sit_8.y = height_scale(350, self.hauteur_actuelle)
                Global_objects.sit_8.draw()

            case 9:
                Global_objects.sit_1.x = width_scale(840, self.largeur_actuelle)
                Global_objects.sit_1.y = height_scale(200, self.hauteur_actuelle)
                Global_objects.sit_1.draw()
                Global_objects.sit_2.x = width_scale(1160, self.largeur_actuelle)
                Global_objects.sit_2.y = height_scale(260, self.hauteur_actuelle)
                Global_objects.sit_2.draw()
                Global_objects.sit_3.x = width_scale(1450, self.largeur_actuelle)
                Global_objects.sit_3.y = height_scale(410, self.hauteur_actuelle)
                Global_objects.sit_3.draw()
                Global_objects.sit_4.x = width_scale(1450, self.largeur_actuelle)
                Global_objects.sit_4.y = height_scale(610, self.hauteur_actuelle)
                Global_objects.sit_4.draw()
                Global_objects.sit_5.x = width_scale(1050, self.largeur_actuelle)
                Global_objects.sit_5.y = height_scale(760, self.hauteur_actuelle)
                Global_objects.sit_5.draw()
                Global_objects.sit_6.x = width_scale(640, self.largeur_actuelle)
                Global_objects.sit_6.y = height_scale(760, self.hauteur_actuelle)
                Global_objects.sit_6.draw()
                Global_objects.sit_7.x = width_scale(230, self.largeur_actuelle)
                Global_objects.sit_7.y = height_scale(610, self.hauteur_actuelle)
                Global_objects.sit_7.draw()
                Global_objects.sit_8.x = width_scale(230, self.largeur_actuelle)
                Global_objects.sit_8.y = height_scale(410, self.hauteur_actuelle)
                Global_objects.sit_8.draw()
                Global_objects.sit_9.x = width_scale(520, self.largeur_actuelle)
                Global_objects.sit_9.y = height_scale(260, self.hauteur_actuelle)
                Global_objects.sit_9.draw()

            case 10:
                Global_objects.sit_1.x = width_scale(680, self.largeur_actuelle)
                Global_objects.sit_1.y = height_scale(190, self.hauteur_actuelle)
                Global_objects.sit_1.draw()
                Global_objects.sit_2.x = width_scale(1010, self.largeur_actuelle)
                Global_objects.sit_2.y = height_scale(190, self.hauteur_actuelle)
                Global_objects.sit_2.draw()
                Global_objects.sit_3.x = width_scale(1300, self.largeur_actuelle)
                Global_objects.sit_3.y = height_scale(340, self.hauteur_actuelle)
                Global_objects.sit_3.draw()
                Global_objects.sit_4.x = width_scale(1550, self.largeur_actuelle)
                Global_objects.sit_4.y = height_scale(450, self.hauteur_actuelle)
                Global_objects.sit_4.draw()
                Global_objects.sit_5.x = width_scale(1300, self.largeur_actuelle)
                Global_objects.sit_5.y = height_scale(640, self.hauteur_actuelle)
                Global_objects.sit_5.draw()
                Global_objects.sit_6.x = width_scale(1010, self.largeur_actuelle)
                Global_objects.sit_6.y = height_scale(790, self.hauteur_actuelle)
                Global_objects.sit_6.draw()
                Global_objects.sit_7.x = width_scale(680, self.largeur_actuelle)
                Global_objects.sit_7.y = height_scale(790, self.hauteur_actuelle)
                Global_objects.sit_7.draw()
                Global_objects.sit_8.x = width_scale(380, self.largeur_actuelle)
                Global_objects.sit_8.y = height_scale(640, self.hauteur_actuelle)
                Global_objects.sit_8.draw()
                Global_objects.sit_9.x = width_scale(140, self.largeur_actuelle)
                Global_objects.sit_9.y = height_scale(530, self.hauteur_actuelle)
                Global_objects.sit_9.draw()
                Global_objects.sit_10.x = width_scale(380, self.largeur_actuelle)
                Global_objects.sit_10.y = height_scale(340, self.hauteur_actuelle)
                Global_objects.sit_10.draw()

        # Dessin de la raise_bar pour choisir le montant
        if self.is_raising:
            gui_font = pygame.font.SysFont("Roboto", width_scale(60, self.largeur_actuelle))
            text_surf = gui_font.render("Choose the bet", True, "#FFFFFF")
            raise_background = pygame.draw.rect(self.screen, "#000000", pygame.Rect((width_scale(340, self.largeur_actuelle), height_scale(300, self.hauteur_actuelle)), (width_scale(1250, self.largeur_actuelle), height_scale(300, self.hauteur_actuelle))), border_radius = 3)
            self.screen.blit(text_surf, (width_scale(820, self.largeur_actuelle), height_scale(320, self.hauteur_actuelle)))
            Global_objects.raise_bar.draw(round(((Global_objects.connected_account[2]/100)*self.raised_amount)*100), width_scale(25, self.largeur_actuelle), width_scale(25, self.largeur_actuelle), height_scale(2.8, self.hauteur_actuelle))
            self.raised_amount = (Global_objects.raise_bar.cursor_width - width_scale(400, self.largeur_actuelle)) / (width_scale(1530, self.largeur_actuelle) - width_scale(400, self.largeur_actuelle))
            Global_objects.confirmraisebutton.draw()
            Global_objects.cancelraisebutton.draw()
            Global_objects.all_inbutton.draw()
            Global_objects.minus100button.draw()
            Global_objects.add100button.draw()
            Global_objects.raiseamountinput.draw()
            # On gére le cas où l'utilisateur garde appuyé la touche backspace
            try:
                if Global_objects.raiseamountinput.backspace:
                    if time.time() >= Global_objects.backspace_timer:
                        Global_objects.raiseamountinput.user_text = Global_objects.raiseamountinput.user_text[:-1]
                        Global_objects.backspace_timer = time.time() + 0.1
            except:
                pass
            # On récupére la position de la souris
            mouse_pos = pygame.mouse.get_pos()
            # On vérifie si la position de la souris est sur le fond noir de la zone pour raise et si non et que l'utilisateur clique, la zone disparait et tout redevient cliquable
            if not raise_background.collidepoint(mouse_pos) and not Global_objects.raise_bar.is_selected and not Global_objects.confirmraisebutton.is_pressing and not Global_objects.cancelraisebutton.is_pressing and not Global_objects.all_inbutton.is_pressing and not Global_objects.minus100button.is_pressing and not Global_objects.add100button.is_pressing:
                # On vérifie si l'utilisateur clique sur le clic gauche ([0] = gauche, [1] = molette, [2] = droit)
                if pygame.mouse.get_pressed()[0]:
                    self.is_raising = False
                    self.timer = [0.5, time.time(), True]
        """elif not self.is_raising and self.round_started and self.timer[0] > 0:
            self.timer[0] = 0.5 - (time.time() - self.timer[1])
            Global_objects.buttons_interactibles = True"""

        # Affichage d'une fenêtre de vérification si l'utilisateur clique sur le bouton leavegamebutton
        if self.confirmation:
            gui_font = pygame.font.SysFont("Roboto", width_scale(60, self.largeur_actuelle))
            text_surf = gui_font.render("IF YOU QUIT YOU WILL LOSE EVERYTHING YOU PUT ON THE LINE.", True, "#FFFFFF")
            pygame.draw.rect(self.screen, "#000000", pygame.Rect((width_scale(280, self.largeur_actuelle), height_scale(400, self.hauteur_actuelle)), (width_scale(1360, self.largeur_actuelle), height_scale(170, self.hauteur_actuelle))), border_radius = 3)
            self.screen.blit(text_surf, (width_scale(290, self.largeur_actuelle), height_scale(410, self.hauteur_actuelle)))
            Global_objects.yesleavebutton.draw()
            Global_objects.noleavebutton.draw()

        # Affichage des boutons par dessus tout le reste
        # Cliquer sur le bouton gamesettingsbutton affiche le menu des paramètres pendant la partie
        Global_objects.gamesettingsbutton.draw()
        # Cliquer sur le bouton leavegamebutton retourne au menu principal
        Global_objects.leavegamebutton.draw()

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
            case "Shop Menu":
                self.shopmenu()
            case "Create Menu":
                self.createtable()
            case "Game Menu":
                self.gamemenu()