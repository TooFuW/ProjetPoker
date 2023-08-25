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
from random import *
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


    # Récupération de la liste des lobbys disponibles et de leurs informations ([0] = Nom de la table, [1] = Nombre de joueurs/nombre de joueurs max, [2] = Montant de la mise, [3] = Pot moyen, [4] = Tapis moyen, [5] = ID de la table)
    displayed_lobbys_list = [["Table 1", "0/5", "50/100", "15K", "25K", "ID1"], ["Table 2", "1/6", "50/100", "10K", "20K", "ID2"], ["Table 3", "2/7", "50/100", "20K", "30K", "ID3"], ["Table 4", "3/8", "50/100", "5K", "15K", "ID4"], ["Table 5", "4/9", "50/100", "8K", "18K", "ID5"], ["Table 6", "5/9", "50/100", "8K", "18K", "ID6"], ["Table 7", "6/9", "50/100", "11K", "21K", "ID7"], ["Table 8", "7/9", "50/100", "18K", "28K", "ID8"], ["Table 9", "8/9", "50/100", "12K", "22K", "ID9"], ["Table 10", "9/9", "50/100", "3K", "13K", "ID10"], ["Table 11", "0/6", "50/100", "15K", "25K", "ID11"], ["Table 12", "1/7", "50/100", "10K", "20K", "ID12"], ["Table 13", "2/8", "50/100", "20K", "30K", "ID13"], ["Table 14", "3/9", "50/100", "5K", "15K", "ID14"], ["Table 15", "4/9", "50/100", "8K", "18K", "ID15"], ["Table 16", "5/9", "50/100", "8K", "18K", "ID16"], ["Table 17", "6/9", "50/100", "11K", "21K", "ID17"], ["Table 18", "7/9", "50/100", "18K", "28K", "ID18"], ["Table 19", "8/9", "50/100", "12K", "22K", "ID19"], ["Table 20", "9/9", "50/100", "3K", "13K", "ID20"]]
    # On initialise globalement displayed_lobbys_list ici car plus bas une erreur se produit
    Global_objects.displayed_lobbys_list = displayed_lobbys_list

    # Chargement de l'image de fond
    pokerbackground = pygame.image.load("Affichage\PokerBackground.jpg")
    fond = pygame.transform.scale(pokerbackground, (screen_width, screen_height))

    # Chargement de l'image de fond en jeu
    pokertable = pygame.image.load("Affichage\PokerTable.png")
    table_fond = pygame.transform.scale(pokertable, (width_scale(1500, largeur_actuelle), screen_height))

    # Chargement du logo du jeu
    logojeu = pygame.image.load("Affichage\PokerBackground.jpg")
    logojeu = pygame.transform.scale(logojeu, (width_scale(250, largeur_actuelle), height_scale(250, hauteur_actuelle)))

    # Chargement du logo MWTE
    logomwte = pygame.image.load("Affichage\logo mwte.jpg")
    logomwte = pygame.transform.scale(logomwte, (width_scale(175, largeur_actuelle), height_scale(175, hauteur_actuelle)))
    logomwte_rect = logomwte.get_rect()
    logomwte_rect.topleft = (width_scale(10, largeur_actuelle), height_scale(890, hauteur_actuelle))

    # Chargement de la photo de profil du joueur
    pdpplayer = pygame.image.load("Affichage\logo mwte.jpg")
    pdpplayer = pygame.transform.scale(pdpplayer, (width_scale(300, largeur_actuelle), height_scale(300, hauteur_actuelle)))

    # Chargement de l'icône MUTE et SOUND:
    iconmute = pygame.image.load("Affichage\mute_icon.png")
    iconmute = pygame.transform.scale(iconmute, (width_scale(50, largeur_actuelle), height_scale(50, hauteur_actuelle)))
    iconsound = pygame.image.load("Affichage\sound_icon.png")
    iconsound = pygame.transform.scale(iconsound, (width_scale(50, largeur_actuelle), height_scale(50, hauteur_actuelle)))

    # Initialisation de la fenêtre actuelle
    game_state = HUD_State(largeur_actuelle, hauteur_actuelle, screen, fond, logojeu, logomwte, logomwte_rect, pdpplayer, table_fond, iconmute, iconsound)

    # Création de tout les boutons utilisés
    # Création de l'objet accountbutton
    accountbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "account", "ACCOUNT", "Roboto", 30, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 150, 75, (1750, 20), 3, 10)
    # Création de l'objet playbutton
    playbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "play", "PLAY", "Roboto", 150, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 500, 500, (710, 365), 6, 10)
    # Création de l'objet settingsbutton
    settingsbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "settings", "SETTINGS", "Roboto", 70, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 300, 500, (310, 365), 6, 10)
    # Création de l'objet quitbutton
    exitbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "exit", "EXIT", "Roboto", 70, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 400, 100, (760, 960), 6, 10)
    # Création de l'objet backbutton
    backbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "back", "", "Roboto", 0, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 125, 125, (25, 25), 6, 10, "Affichage\\backarrow.png")
    # Création de l'objet createtablebutton
    createtablebutton = Button(largeur_actuelle, hauteur_actuelle, screen, "create table", "CREATE TABLE", "Roboto", 60, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 400, 100, (175, 50), 6, 10)
    # Création de l'objet gamehistorybutton
    gamehistorybutton = Button(largeur_actuelle, hauteur_actuelle, screen, "history", "HISTORY", "Roboto", 70, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 300, 500, (1310, 365), 6, 10)
    # Création de l'objet deconnexionbutton
    deconnexionbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "deconnexion", "LOG OUT", "Roboto", 60, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 300, 100, (1605, 970), 6, 10)
    # Création de l'objet accountsettingsbutton
    accountsettingsbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "account settings", "", "Roboto", 0, "#D74B4B", "#D74B4B", "#D74B4B", "#D74B4B", 125, 125, (1770, 25), 0, 10, "Affichage\\settinglogo.png")
    # Création de l'objet settingpage1button
    settingpage1button = Button(largeur_actuelle, hauteur_actuelle, screen, "setting page 1", "PAGE 1", "Roboto", 50, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 200, 70, (260, 90), 4, 8)
    # Création de l'objet settingpage1button
    settingpage2button = Button(largeur_actuelle, hauteur_actuelle, screen, "setting page 2", "PAGE 2", "Roboto", 50, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 200, 70, (470, 90), 4, 8)
    # Création de l'objet settingpage1button
    settingpage3button = Button(largeur_actuelle, hauteur_actuelle, screen, "setting page 3", "PAGE 3", "Roboto", 50, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 200, 70, (680, 90), 4, 8)
    # Création de l'objet gamesettingsbutton
    gamesettingsbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "game settings", "", "Roboto", 0, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 125, 125, (1770, 25), 6, 10, "Affichage\\settinglogo.png")
    # Création de l'objet checkbutton
    checkbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "check", "CHECK", "Roboto", 60, "#4CAF50", "#4CAF50", "#00FF00", "#4CAF50", 355, 100, (1540, 190), 6, 10)
    # Création de l'objet callbutton
    callbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "call", "CALL", "Roboto", 60, "#FFD700", "#FFD700", "#FFFF00", "#FFD700", 355, 100, (1540, 340), 6, 10)
    # Création de l'objet laybutton
    laybutton = Button(largeur_actuelle, hauteur_actuelle, screen, "lay", "LAY", "Roboto", 60, "#0000FF", "#0000FF", "#0074D9", "#0000FF", 355, 100, (1540, 490), 6, 10)
    # Création de l'objet raisebutton
    raisebutton = Button(largeur_actuelle, hauteur_actuelle, screen, "raise", "RAISE", "Roboto", 60, "#D32F2A", "#D32F2A", "#FF4F58", "#D32F2A", 355, 100, (1540, 640), 6, 10)
    

    # Création des scrollboxs
    # Création de l'objet serverscrollbox 
    serverscrollbox = ScrollBox(largeur_actuelle, hauteur_actuelle, screen, 210, 215, 1000, 760, Global_objects.displayed_lobbys_list)
    # Création de l'objet historyscrollbox
    historyscrollbox = ScrollBox(largeur_actuelle, hauteur_actuelle, screen, 210, 215, 1000, 760, Global_objects.displayed_lobbys_list)

    # Création des TextInputBox
    # Création de l'objet tablecodeinput
    tablecodeinput = TextInputBox(largeur_actuelle, hauteur_actuelle, screen, 150, (1360, 890), 400, 100, "#333333", "#888888", 400, False, 6, True)
    # Création de l'objet accountpseudoinput
    accountpseudoinput = TextInputBox(largeur_actuelle, hauteur_actuelle, screen, 60, (685, 190), 600, 100, "#333333", "#475F77", 600, False, 10, False, False, "PSEUDO")
    # Création de l'objet accountinformationinput
    accountinformationinput = TextInputBox(largeur_actuelle, hauteur_actuelle, screen, 60, (685, 315), 600, 650, "#333333", "#475F77", 600, False, 100, False, False, "INFORMATIONS")

    # Création des previews de tables
    # Création de l'objet previewlobbys
    previewlobbys = Preview_Table(largeur_actuelle, hauteur_actuelle, screen, (1310, 215))
    # Création de l'objet previewhistory
    previewhistory = Preview_Table(largeur_actuelle, hauteur_actuelle, screen, (1310, 215))

    # Initialisation de toutes les valeurs globales stockées dans le fichier Global_objects.py (tous les objets que l'on crée ci-dessus)
    Global_objects.game_state = game_state
    Global_objects.accountbutton = accountbutton
    Global_objects.playbutton = playbutton
    Global_objects.settingsbutton = settingsbutton
    Global_objects.exitbutton = exitbutton
    Global_objects.backbutton = backbutton
    Global_objects.createtablebutton = createtablebutton
    Global_objects.gamehistorybutton = gamehistorybutton
    Global_objects.deconnexionbutton = deconnexionbutton
    Global_objects.accountsettingsbutton = accountsettingsbutton
    Global_objects.settingpage1button = settingpage1button
    Global_objects.settingpage2button = settingpage2button
    Global_objects.settingpage3button = settingpage3button
    Global_objects.serverscrollbox = serverscrollbox
    Global_objects.historyscrollbox = historyscrollbox
    Global_objects.tablecodeinput = tablecodeinput
    Global_objects.accountpseudoinput = accountpseudoinput
    Global_objects.accountinformationinput = accountinformationinput
    Global_objects.previewlobbys = previewlobbys
    Global_objects.previewhistory = previewhistory
    Global_objects.gamesettingsbutton = gamesettingsbutton
    Global_objects.checkbutton = checkbutton
    Global_objects.callbutton = callbutton
    Global_objects.laybutton = laybutton
    Global_objects.raisebutton = raisebutton
    Global_objects.volume_music = 1.0
    Global_objects.buttons_interactibles = True
    Global_objects.displayed_lobbys_list = displayed_lobbys_list

    # Gameloop
    while True:
        largeur_actuelle = screen.get_width()
        hauteur_actuelle = screen.get_height()
        # Chargement de la musique de fond et mise en boucle
        pygame.mixer.music.set_volume(Global_objects.volume_music)
        if pygame.mixer.music.get_busy() != True:
            pygame.mixer.music.load("Affichage\mainmenu_soundtrack.mp3")
            pygame.mixer.music.rewind()
            pygame.mixer.music.play()
        # Cet appel permet de gérer l'interface active
        game_state.state_manager()
        # Limite les FPS à 60
        clock.tick(120)