"""Document contenant le fichier principal à exécuter pour lancer le jeu"""


import pygame
from Screen_adaptation import *
from Button_class import *
from Scrollbox_class import *
from TextInputBox_class import *
from Preview_Table_class import *
from HUD_State_class import *
from Cursor_Bar_class import *
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
    saved_largeur = largeur_actuelle
    saved_hauteur = hauteur_actuelle
    # Nom de la fenêtre
    pygame.display.set_caption("MWTE Poker")
    clock = pygame.time.Clock()

    # On initialise current_folder pour faciliter la manipulation des chemins d'accès
    current_folder = __file__[:-7]

    # Récupération de la liste des lobbys disponibles et de leurs informations ([0] = Nom de la table, [1] = Nombre de joueurs/nombre de joueurs max, [2] = Montant de la mise, [3] = Pot moyen, [4] = Tapis moyen, [5] = ID de la table)
    # On initialise globalement displayed_lobbys_list ici car plus bas une erreur se produit
    Global_objects.displayed_lobbys_list = [["Table 1", "0/5", "50/100", "15K", "25K", "1"], ["Table 2", "1/6", "50/100", "10K", "20K", "2"], ["Table 3", "2/7", "50/100", "20K", "30K", "3"], ["Table 4", "3/8", "50/100", "5K", "15K", "4"], ["Table 5", "4/9", "50/100", "8K", "18K", "5"], ["Table 6", "5/9", "50/100", "8K", "18K", "6"], ["Table 7", "6/9", "50/100", "11K", "21K", "7"], ["Table 8", "7/9", "50/100", "18K", "28K", "8"], ["Table 9", "8/9", "50/100", "12K", "22K", "9"], ["Table 10", "9/9", "50/100", "3K", "13K", "10"], ["Table 11", "0/6", "50/100", "15K", "25K", "11"], ["Table 12", "1/7", "50/100", "10K", "20K", "12"], ["Table 13", "2/8", "50/100", "20K", "30K", "13"], ["Table 14", "3/9", "50/100", "5K", "15K", "14"], ["Table 15", "4/9", "50/100", "8K", "18K", "15"], ["Table 16", "5/9", "50/100", "8K", "18K", "16"], ["Table 17", "6/9", "50/100", "11K", "21K", "17"], ["Table 18", "7/9", "50/100", "18K", "28K", "18"], ["Table 19", "8/9", "50/100", "12K", "22K", "19"], ["Table 20", "9/9", "50/100", "3K", "13K", "20"]]

    # Chargement de l'image de fond
    pokerbackground = pygame.image.load(current_folder + "PokerBackground.jpg")
    fond = pygame.transform.scale(pokerbackground, (largeur_actuelle, hauteur_actuelle))

    # Chargement de l'image de fond en jeu
    pokertable = pygame.image.load(current_folder + "PokerTable.png")
    table_fond = pygame.transform.scale(pokertable, (largeur_actuelle, hauteur_actuelle))

    # Chargement du logo du jeu
    logojeu = pygame.image.load(current_folder + "logo jeu.jpg")
    logojeu = pygame.transform.scale(logojeu, (width_scale(750, largeur_actuelle), height_scale(500, hauteur_actuelle)))

    # Chargement du logo MWTE
    logomwte = pygame.image.load(current_folder + "logo mwte.jpg")
    logomwte = pygame.transform.scale(logomwte, (width_scale(175, largeur_actuelle), height_scale(175, hauteur_actuelle)))
    logomwte_rect = logomwte.get_rect()
    logomwte_rect.topleft = (width_scale(10, largeur_actuelle), height_scale(890, hauteur_actuelle))
    # On change l'îcone du jeu pour le logo MWTE
    pygame.display.set_icon(logomwte)

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

    # On charge les images des cartes dans le dictionnaire Global_objects.cards
    Global_objects.cards = {"1c" : pygame.image.load(current_folder + "Cards\\Ac.png"),
                            "1d" : pygame.image.load(current_folder + "Cards\\Ad.png"),
                            "1h" : pygame.image.load(current_folder + "Cards\\Ah.png"),
                            "1s" : pygame.image.load(current_folder + "Cards\\As.png"),
                            "2c" : pygame.image.load(current_folder + "Cards\\2c.png"),
                            "2d" : pygame.image.load(current_folder + "Cards\\2d.png"),
                            "2h" : pygame.image.load(current_folder + "Cards\\2h.png"),
                            "2s" : pygame.image.load(current_folder + "Cards\\2s.png"),
                            "3c" : pygame.image.load(current_folder + "Cards\\3c.png"),
                            "3d" : pygame.image.load(current_folder + "Cards\\3d.png"),
                            "3h" : pygame.image.load(current_folder + "Cards\\3h.png"),
                            "3s" : pygame.image.load(current_folder + "Cards\\3s.png"),
                            "4c" : pygame.image.load(current_folder + "Cards\\4c.png"),
                            "4d" : pygame.image.load(current_folder + "Cards\\4d.png"),
                            "4h" : pygame.image.load(current_folder + "Cards\\4h.png"),
                            "4s" : pygame.image.load(current_folder + "Cards\\4s.png"),
                            "5c" : pygame.image.load(current_folder + "Cards\\5c.png"),
                            "5d" : pygame.image.load(current_folder + "Cards\\5d.png"),
                            "5h" : pygame.image.load(current_folder + "Cards\\5h.png"),
                            "5s" : pygame.image.load(current_folder + "Cards\\5s.png"),
                            "6c" : pygame.image.load(current_folder + "Cards\\6c.png"),
                            "6d" : pygame.image.load(current_folder + "Cards\\6d.png"),
                            "6h" : pygame.image.load(current_folder + "Cards\\6h.png"),
                            "6s" : pygame.image.load(current_folder + "Cards\\6s.png"),
                            "7c" : pygame.image.load(current_folder + "Cards\\7c.png"),
                            "7d" : pygame.image.load(current_folder + "Cards\\7d.png"),
                            "7h" : pygame.image.load(current_folder + "Cards\\7h.png"),
                            "7s" : pygame.image.load(current_folder + "Cards\\7s.png"),
                            "8c" : pygame.image.load(current_folder + "Cards\\8c.png"),
                            "8d" : pygame.image.load(current_folder + "Cards\\8d.png"),
                            "8h" : pygame.image.load(current_folder + "Cards\\8h.png"),
                            "8s" : pygame.image.load(current_folder + "Cards\\8s.png"),
                            "9c" : pygame.image.load(current_folder + "Cards\\9c.png"),
                            "9d" : pygame.image.load(current_folder + "Cards\\9d.png"),
                            "9h" : pygame.image.load(current_folder + "Cards\\9h.png"),
                            "9s" : pygame.image.load(current_folder + "Cards\\9s.png"),
                            "tc" : pygame.image.load(current_folder + "Cards\\10c.png"),
                            "td" : pygame.image.load(current_folder + "Cards\\10d.png"),
                            "th" : pygame.image.load(current_folder + "Cards\\10h.png"),
                            "ts" : pygame.image.load(current_folder + "Cards\\10s.png"),
                            "jc" : pygame.image.load(current_folder + "Cards\\jc.png"),
                            "jd" : pygame.image.load(current_folder + "Cards\\jd.png"),
                            "jh" : pygame.image.load(current_folder + "Cards\\jh.png"),
                            "js" : pygame.image.load(current_folder + "Cards\\js.png"),
                            "qc" : pygame.image.load(current_folder + "Cards\\Qc.png"),
                            "qd" : pygame.image.load(current_folder + "Cards\\Qd.png"),
                            "qh" : pygame.image.load(current_folder + "Cards\\Qh.png"),
                            "qs" : pygame.image.load(current_folder + "Cards\\Qs.png"),
                            "kc" : pygame.image.load(current_folder + "Cards\\Kc.png"),
                            "kd" : pygame.image.load(current_folder + "Cards\\Kd.png"),
                            "kh" : pygame.image.load(current_folder + "Cards\\Kh.png"),
                            "ks" : pygame.image.load(current_folder + "Cards\\Ks.png"),
                            "dos" : pygame.image.load(current_folder + "Cards\\Dos.png")}

    # Initialisation de la fenêtre actuelle
    Global_objects.game_state = HUD_State(largeur_actuelle, hauteur_actuelle, screen, fond, logojeu, logomwte, logomwte_rect, pdpplayer, table_fond, [iconsound_mute, iconsound_low, iconsound_mid, iconsound_max])

    # Création de tout les boutons utilisés
    # Création de l'objet accountbutton
    Global_objects.accountbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "account", "ACCOUNT", "Roboto", 30, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 150, 75, (1750, 20), 3, 10)
    # Création de l'objet playbutton
    Global_objects.playbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "play", "", "Roboto", 0, "#000000", "#000000", "#404040", "#404040", 500, 500, (710, 365), 6, 400, current_folder + "logo play.jpg")
    # Création de l'objet settingsbutton
    Global_objects.settingsbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "settings", "SETTINGS", "Roboto", 70, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 300, 500, (310, 365), 6, 10)
    # Création de l'objet quitbutton
    Global_objects.exitbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "exit", "", "Roboto", 0, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 400, 100, (760, 960), 6, 10, current_folder + "logo exit.jpg")
    # Création de l'objet backbutton
    Global_objects.backbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "back", "", "Roboto", 0, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 125, 125, (25, 25), 6, 10, current_folder + "backarrow.png")
    # Création de l'objet createtablebutton
    Global_objects.createtablebutton = Button(largeur_actuelle, hauteur_actuelle, screen, "create table", "CREATE TABLE", "Roboto", 60, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 400, 100, (175, 50), 6, 10)
    # Création de l'objet shopbutton
    Global_objects.shopbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "shop", "SHOP", "Roboto", 70, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 300, 500, (1310, 365), 6, 10)
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
    # Création de l'objet leavegamebutton
    Global_objects.leavegamebutton = Button(largeur_actuelle, hauteur_actuelle, screen, "leave game", "", "Roboto", 0, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 80, 80, (1720, 995), 4, 10, current_folder + "backarrow.png")
    # Création de l'objet yesleavebutton
    Global_objects.yesleavebutton = Button(largeur_actuelle, hauteur_actuelle, screen, "yes_leave", "YES", "Roboto", 60, "#4CAF50", "#4CAF50", "#00FF00", "#4CAF50", 150, 70, (790, 480), 3, 10)
    # Création de l'objet noleavebutton
    Global_objects.noleavebutton = Button(largeur_actuelle, hauteur_actuelle, screen, "no_leave", "NO", "Roboto", 60, "#D32F2A", "#D32F2A", "#FF4F58", "#D32F2A", 150, 70, (990, 480), 3, 10)
    # Création de l'objet sit_upbutton
    Global_objects.sit_upbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "sit up", "SIT UP", "Roboto", 60, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 250, 80, (1425, 995), 6, 10)
    # Création de l'objet minus100button
    Global_objects.minus100button = Button(largeur_actuelle, hauteur_actuelle, screen, "minus_100", "- 100", "Roboto", 60, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 150, 70, (355, 520), 3, 10)
    # Création de l'objet add100button
    Global_objects.add100button = Button(largeur_actuelle, hauteur_actuelle, screen, "add_100", "+ 100", "Roboto", 60, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 150, 70, (815, 520), 3, 10)
    # Création de l'objet all_inbutton
    Global_objects.all_inbutton = Button(largeur_actuelle, hauteur_actuelle, screen, "all_in", "ALL IN", "Roboto", 60, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 150, 70, (985, 520), 3, 10)
    # Création de l'objet confirmraisebutton
    Global_objects.confirmraisebutton = Button(largeur_actuelle, hauteur_actuelle, screen, "yes_raise", "CONFIRM", "Roboto", 60, "#4CAF50", "#4CAF50", "#00FF00", "#4CAF50", 200, 70, (1155, 520), 3, 10)
    # Création de l'objet cancelraisebutton
    Global_objects.cancelraisebutton = Button(largeur_actuelle, hauteur_actuelle, screen, "no_raise", "CANCEL", "Roboto", 60, "#D32F2A", "#D32F2A", "#FF4F58", "#D32F2A", 200, 70, (1375, 520), 3, 10)

    # Raccourcis clavier pour les boutons
    Global_objects.raccourcis_gamemenu = {"c" : Global_objects.checkbutton,
                                        "v" : Global_objects.callbutton,
                                        "b" : Global_objects.foldbutton,
                                        "n" : Global_objects.raisebutton,}

    # Création des Scrollboxs
    # Création de l'objet serverscrollbox 
    Global_objects.serverscrollbox = ScrollBox(largeur_actuelle, hauteur_actuelle, screen, 210, 240, 1000, 760, Global_objects.displayed_lobbys_list)
    
    # Création des TextInputBox
    # Création de l'objet tablecodeinput
    Global_objects.tablecodeinput = TextInputBox(largeur_actuelle, hauteur_actuelle, screen, 150, (1360, 890), 400, 100, "#333333", "#888888", 400, False, 6, True)
    # Création de l'objet accountpseudoinput
    Global_objects.accountpseudoinput = TextInputBox(largeur_actuelle, hauteur_actuelle, screen, 60, (685, 190), 600, 100, "#333333", "#475F77", 600, False, 15, False, False, "PSEUDO")
    # Création de l'objet accountinformationinput
    Global_objects.accountinformationinput = TextInputBox(largeur_actuelle, hauteur_actuelle, screen, 60, (685, 315), 600, 650, "#333333", "#475F77", 600, False, 100, False, False, "INFORMATIONS")
    # Création de l'objet raiseamountinput
    Global_objects.raiseamountinput = TextInputBox(largeur_actuelle, hauteur_actuelle, screen, 100, (525, 518), 270, 72, "#333333", "#888888", 270, False, 6, True)

    # Création des Previews_Table
    # Création de l'objet previewlobbys
    Global_objects.previewlobbys = Preview_Table(largeur_actuelle, hauteur_actuelle, screen, table_fond, (1270, 215))

    # Création des sits
    # Création de l'objet sit_1
    Global_objects.sit_1 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0), pdpplayer)
    # Création de l'objet sit_2
    Global_objects.sit_2 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0), pdpplayer)
    # Création de l'objet sit_3
    Global_objects.sit_3 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0), pdpplayer)
    # Création de l'objet sit_4
    Global_objects.sit_4 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0), pdpplayer)
    # Création de l'objet sit_5
    Global_objects.sit_5 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0), pdpplayer)
    # Création de l'objet sit_6
    Global_objects.sit_6 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0), pdpplayer)
    # Création de l'objet sit_6
    Global_objects.sit_6 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0), pdpplayer)
    # Création de l'objet sit_7
    Global_objects.sit_7 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0), pdpplayer)
    # Création de l'objet sit_8
    Global_objects.sit_8 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0), pdpplayer)
    # Création de l'objet sit_9
    Global_objects.sit_9 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0), pdpplayer)
    # Création de l'objet sit_10
    Global_objects.sit_10 = Sits(largeur_actuelle, hauteur_actuelle, screen, 250, 80, (0, 0), pdpplayer)

    # Création des cursor_bar
    # Création de l'objet sound_bar
    Global_objects.sound_bar = Cursor_Bar(largeur_actuelle, hauteur_actuelle, screen, 200, 15, (500, 198), "#FFFFFF", "#FFFFFF", "#000000", 700)
    # Création de l'objet raise_bar
    Global_objects.raise_bar = Cursor_Bar(largeur_actuelle, hauteur_actuelle, screen, 1130, 30, (400, 400), "#FFFFFF", "#FFFFFF", "#000000", 400)

    # Initialisation des autres variables globales stockées dans le fichier Global_objects.py
    Global_objects.volume_music = 1.0
    Global_objects.buttons_interactibles = True
    # Permet de savoir si [0] l'utilisateur est entrain de sélectionner un siège, [1] quel siège il a sélectionné
    Global_objects.is_selecting_sit = [False, -1]
    # Initialisation du dictionnaire global qui permettra aux paquets de correspondre avec la fonction qui l'appelle
    Global_objects.func_id_dict = {}
    # Initialisation des sièges arrivés automatiquement
    Global_objects.auto_arrived_sits = []
    # Initialisation de la référence du client actuel
    Global_objects.client_actuel = 0
    # Pour savoir qui a la parole (= entier qui est le numéro du siège qui a la parole) (sur 1 pour l'instant pour faire les tests)
    Global_objects.parole = 1
    # Pot de la partie
    Global_objects.pot = 0
    # Cartes du client
    Global_objects.card_1 = None
    Global_objects.card_2 = None
    # Nombre de cartes à afficher (que les joueurs ont en main)
    Global_objects.nombre_cartes = 0
    # Délai entre 2 caractéres supprimés pour les TextInputBox
    Global_objects.backspace_timer = time.time() + 0.1
    # Infos du client/joueur connecté sous la forme [idplayer, pseudo, chips, link]
    Global_objects.connected_account = [None, "dummy", 1500, "link"]
    # Objet Sit actif
    Global_objects.active_sit = None

    # Gameloop
    while True:
        largeur_actuelle = screen.get_width()
        hauteur_actuelle = screen.get_height()
        # Changer tous les objets affichés pour qu'ils aient la bonne taille
        if largeur_actuelle != saved_largeur or hauteur_actuelle != saved_hauteur:
            pass
        saved_largeur = largeur_actuelle
        saved_hauteur = hauteur_actuelle
        # Chargement de la musique de fond et mise en boucle
        pygame.mixer.music.set_volume(Global_objects.volume_music)
        if pygame.mixer.music.get_busy() != True:
            pygame.mixer.music.load(current_folder + "mainmenu_soundtrack.mp3")
            pygame.mixer.music.rewind()
            pygame.mixer.music.play()
        # Cet appel permet de gérer l'interface active
        Global_objects.game_state.state_manager()
        # Définit les FPS à 120 pour plus de fluidité (60 par défaut)
        clock.tick(120)