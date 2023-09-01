#Menu du jeu Poker 


import pygame
from Screen_adaptation import *
from Button_class import *
from Scrollbox_class import *
from TextInputBox_class import *
from Preview_Table_class import *
from HUD_State_class import *
import Global_objects
from socket import *
from threading import *
from packet_separator import *
from network import *


if __name__ == "__main__":
    # Taille de la fenêtre
    pygame.init()
    start_client()
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    largeur_actuelle = screen.get_width()
    hauteur_actuelle = screen.get_height()
    # Nom de la fenêtre
    pygame.display.set_caption("Menu Jeu Poker")
    clock = pygame.time.Clock()

    # On initialise current_folder pour faciliter la manipulation des chemins d'accès
    current_folder = __file__[:-7]

    # Récupération de la liste des lobbys disponibles et de leurs informations ([0] = Nom de la table, [1] = Nombre de joueurs/nombre de joueurs max, [2] = Montant de la mise, [3] = Pot moyen, [4] = Tapis moyen, [5] = ID de la table)
    # On initialise globalement displayed_lobbys_list ici car plus bas une erreur se produit
    Global_objects.displayed_lobbys_list = [["Table 1", "0/5", "50/100", "15K", "25K", "1"], ["Table 2", "1/6", "50/100", "10K", "20K", "2"], ["Table 3", "2/7", "50/100", "20K", "30K", "3"], ["Table 4", "3/8", "50/100", "5K", "15K", "4"], ["Table 5", "4/9", "50/100", "8K", "18K", "5"], ["Table 6", "5/9", "50/100", "8K", "18K", "6"], ["Table 7", "6/9", "50/100", "11K", "21K", "7"], ["Table 8", "7/9", "50/100", "18K", "28K", "8"], ["Table 9", "8/9", "50/100", "12K", "22K", "9"], ["Table 10", "9/9", "50/100", "3K", "13K", "10"], ["Table 11", "0/6", "50/100", "15K", "25K", "11"], ["Table 12", "1/7", "50/100", "10K", "20K", "12"], ["Table 13", "2/8", "50/100", "20K", "30K", "13"], ["Table 14", "3/9", "50/100", "5K", "15K", "14"], ["Table 15", "4/9", "50/100", "8K", "18K", "15"], ["Table 16", "5/9", "50/100", "8K", "18K", "16"], ["Table 17", "6/9", "50/100", "11K", "21K", "17"], ["Table 18", "7/9", "50/100", "18K", "28K", "18"], ["Table 19", "8/9", "50/100", "12K", "22K", "19"], ["Table 20", "9/9", "50/100", "3K", "13K", "20"]]

    # Chargement de l'image de fond
    pokerbackground = pygame.image.load(current_folder + "PokerBackground.jpg")
    fond = pygame.transform.scale(pokerbackground, (screen_width, screen_height))

    # Chargement de l'image de fond en jeu
    pokertable = pygame.image.load(current_folder + "PokerTable.png")
    table_fond = pygame.transform.scale(pokertable, (screen_width, screen_height))

    # Chargement du logo du jeu
    logojeu = pygame.image.load(current_folder + "logo jeu.jpg")
    logojeu = pygame.transform.scale(logojeu, (width_scale(750, largeur_actuelle), height_scale(500, hauteur_actuelle)))

    # Chargement du logo MWTE
    logomwte = pygame.image.load(current_folder + "logo mwte.jpg")
    logomwte = pygame.transform.scale(logomwte, (width_scale(175, largeur_actuelle), height_scale(175, hauteur_actuelle)))
    logomwte_rect = logomwte.get_rect()
    logomwte_rect.topleft = (width_scale(10, largeur_actuelle), height_scale(890, hauteur_actuelle))

    # Chargement de la photo de profil du joueur
    pdpplayer = pygame.image.load(current_folder + "logo mwte.jpg")
    pdpplayer = pygame.transform.scale(pdpplayer, (width_scale(300, largeur_actuelle), height_scale(300, hauteur_actuelle)))

    # Chargement des icônes de son:
    iconsound_mute = pygame.image.load(current_folder + "sound_mute.png")
    iconsound_mute = pygame.transform.scale(iconsound_mute, (width_scale(70, largeur_actuelle), height_scale(70, hauteur_actuelle)))
    iconsound_low = pygame.image.load(current_folder + "sound_low.png")
    iconsound_low = pygame.transform.scale(iconsound_low, (width_scale(70, largeur_actuelle), height_scale(70, hauteur_actuelle)))
    iconsound_mid = pygame.image.load(current_folder + "sound_mid.png")
    iconsound_mid = pygame.transform.scale(iconsound_mid, (width_scale(70, largeur_actuelle), height_scale(70, hauteur_actuelle)))
    iconsound_max = pygame.image.load(current_folder + "sound_max.png")
    iconsound_max = pygame.transform.scale(iconsound_max, (width_scale(70, largeur_actuelle), height_scale(70, hauteur_actuelle)))

    # Initialisation de la fenêtre actuelle
    Global_objects.game_state = HUD_State(largeur_actuelle, hauteur_actuelle, screen, fond, logojeu, logomwte, logomwte_rect, pdpplayer, table_fond, [iconsound_mute, iconsound_low, iconsound_mid, iconsound_max])

    # Création de tout les boutons utilisés
    # Création de l'objet accountbutton
    Global_objects.accountbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "account", "ACCOUNT", "Roboto", 30, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 150, 75, (1750, 20), 3, 10)
    # Création de l'objet playbutton
    Global_objects.playbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "play", "PLAY", "Roboto", 150, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 500, 500, (710, 365), 6, 10)
    # Création de l'objet settingsbutton
    Global_objects.settingsbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "settings", "SETTINGS", "Roboto", 70, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 300, 500, (310, 365), 6, 10)
    # Création de l'objet quitbutton
    Global_objects.exitbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "exit", "", "Roboto", 0, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 400, 100, (760, 960), 6, 10, current_folder + "logo exit.jpg")
    # Création de l'objet backbutton
    Global_objects.backbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "back", "", "Roboto", 0, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 125, 125, (25, 25), 6, 10, current_folder + "backarrow.png")
    # Création de l'objet createtablebutton
    Global_objects.createtablebutton = Button(largeur_actuelle, hauteur_actuelle, screen, "create table", "CREATE TABLE", "Roboto", 60, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 400, 100, (175, 50), 6, 10)
    # Création de l'objet gamehistorybutton
    Global_objects.gamehistorybutton = Button(largeur_actuelle, hauteur_actuelle, screen, "history", "HISTORY", "Roboto", 70, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 300, 500, (1310, 365), 6, 10)
    # Création de l'objet deconnexionbutton
    Global_objects.deconnexionbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "deconnexion", "LOG OUT", "Roboto", 60, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 300, 100, (1605, 970), 6, 10)
    # Création de l'objet accountsettingsbutton
    Global_objects.accountsettingsbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "account settings", "", "Roboto", 0, "#D74B4B", "#D74B4B", "#D74B4B", "#D74B4B", 125, 125, (1770, 25), 0, 10, current_folder + "settinglogo.png")
    # Création de l'objet settingpage1button
    Global_objects.settingpage1button = Button(largeur_actuelle, hauteur_actuelle, screen, "setting page 1", "PAGE 1", "Roboto", 50, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 200, 70, (260, 90), 4, 8)
    # Création de l'objet settingpage1button
    Global_objects.settingpage2button = Button(largeur_actuelle, hauteur_actuelle, screen, "setting page 2", "PAGE 2", "Roboto", 50, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 200, 70, (470, 90), 4, 8)
    # Création de l'objet settingpage1button
    Global_objects.settingpage3button = Button(largeur_actuelle, hauteur_actuelle, screen, "setting page 3", "PAGE 3", "Roboto", 50, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 200, 70, (680, 90), 4, 8)
    # Création de l'objet gamesettingsbutton
    Global_objects.gamesettingsbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "game settings", "", "Roboto", 0, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 80, 80, (1820, 995), 4, 10, current_folder + "settinglogo.png")
    # Création de l'objet checkbutton
    Global_objects.checkbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "check", "CHECK", "Roboto", 60, "#4CAF50", "#4CAF50", "#00FF00", "#4CAF50", 300, 80, (30, 995), 6, 10)
    # Création de l'objet callbutton
    Global_objects.callbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "call", "CALL", "Roboto", 60, "#FFD700", "#FFD700", "#FFFF00", "#FFD700", 300, 80, (380, 995), 6, 10)
    # Création de l'objet foldbutton
    Global_objects.foldbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "fold", "FOLD", "Roboto", 60, "#0000FF", "#0000FF", "#0074D9", "#0000FF", 300, 80, (730, 995), 6, 10)
    # Création de l'objet raisebutton
    Global_objects.raisebutton = Button(largeur_actuelle, hauteur_actuelle, screen, "raise", "RAISE", "Roboto", 60, "#D32F2A", "#D32F2A", "#FF4F58", "#D32F2A", 300, 80, (1080, 995), 6, 10)
    # Création de l'objet refreshbutton
    Global_objects.refreshbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "refresh", "REFRESH", "Roboto", 60, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 220, 100, (600, 50), 6, 10)
    

    # Création des Scrollboxs
    # Création de l'objet serverscrollbox 
    Global_objects.serverscrollbox = ScrollBox(largeur_actuelle, hauteur_actuelle, screen, 210, 215, 1000, 760, Global_objects.displayed_lobbys_list)
    # Création de l'objet historyscrollbox
    Global_objects.historyscrollbox = ScrollBox(largeur_actuelle, hauteur_actuelle, screen, 210, 215, 1000, 760, Global_objects.displayed_lobbys_list)

    # Création des TextInputBox
    # Création de l'objet tablecodeinput
    Global_objects.tablecodeinput = TextInputBox(largeur_actuelle, hauteur_actuelle, screen, 150, (1360, 890), 400, 100, "#333333", "#888888", 400, False, 6, True)
    # Création de l'objet accountpseudoinput
    Global_objects.accountpseudoinput = TextInputBox(largeur_actuelle, hauteur_actuelle, screen, 60, (685, 190), 600, 100, "#333333", "#475F77", 600, False, 15, False, False, "PSEUDO")
    # Création de l'objet accountinformationinput
    Global_objects.accountinformationinput = TextInputBox(largeur_actuelle, hauteur_actuelle, screen, 60, (685, 315), 600, 650, "#333333", "#475F77", 600, False, 100, False, False, "INFORMATIONS")

    # Création des Previews_Table
    # Création de l'objet previewlobbys
    Global_objects.previewlobbys = Preview_Table(largeur_actuelle, hauteur_actuelle, screen, table_fond, (1270, 215))
    # Création de l'objet previewhistory
    Global_objects.previewhistory = Preview_Table(largeur_actuelle, hauteur_actuelle, screen, table_fond, (1270, 215))

    # Création des sits
    # Création de l'objet sit_1
    Global_objects.sit_1 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0))
    # Création de l'objet sit_2
    Global_objects.sit_2 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0))
    # Création de l'objet sit_3
    Global_objects.sit_3 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0))
    # Création de l'objet sit_4
    Global_objects.sit_4 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0))
    # Création de l'objet sit_5
    Global_objects.sit_5 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0))
    # Création de l'objet sit_6
    Global_objects.sit_6 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0))
    # Création de l'objet sit_6
    Global_objects.sit_6 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0))
    # Création de l'objet sit_7
    Global_objects.sit_7 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0))
    # Création de l'objet sit_8
    Global_objects.sit_8 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0))
    # Création de l'objet sit_9
    Global_objects.sit_9 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0))
    # Création de l'objet sit_10
    Global_objects.sit_10 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0))

    # Initialisation des autres variables globales stockées dans le fichier Global_objects.py
    Global_objects.volume_music = 1.0
    Global_objects.buttons_interactibles = True

    # Gameloop
    while True:
        largeur_actuelle = screen.get_width()
        hauteur_actuelle = screen.get_height()
        # Chargement de la musique de fond et mise en boucle
        pygame.mixer.music.set_volume(Global_objects.volume_music)
        if pygame.mixer.music.get_busy() != True:
            pygame.mixer.music.load(current_folder + "mainmenu_soundtrack.mp3")
            pygame.mixer.music.rewind()
            pygame.mixer.music.play()
        # Cet appel permet de gérer l'interface active
        Global_objects.game_state.state_manager()
        # Limite les FPS à 120 pour plus de fluidité
        clock.tick(120)