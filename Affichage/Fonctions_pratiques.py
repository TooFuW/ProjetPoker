"""Document contenant des fonctions pratiques afin d'éviter des répétitions dans HUD_State_class.py et réduire le nombre de lignes"""


import pygame
import Global_objects
from TextInputBox_class import *
import time
from network import *


def timer_backspace(text_input : TextInputBox):
    """Timer pour la touche backspace lorsque l'utilisateur écrit

    Args:
        text_input (TextInputBox): TextInputBox avec laquelle on intéragit
    """
    if text_input.backspace:
        if time.time() >= Global_objects.backspace_timer:
            text_input.user_text = text_input.user_text[:-1]
            Global_objects.backspace_timer = time.time() + 0.1

def text_input_write(event : pygame.event.Event, text_input : TextInputBox):
    """Vérification des inputs de l'utilisateur et des conditions de la TextInputBox pour écrire dedans

    Args:
        event (pygame.event.Event): variable des événements pygame
        text_input (TextInputBox): zone de texte à modifier
    """
    if event.type == pygame.KEYDOWN:
        # Si on clique sur supprimer
        if event.key == pygame.K_BACKSPACE:
            text_input.backspace = True
        # Si on clique sur entrer
        elif event.key == pygame.K_RETURN:
            text_input.active = False
            Global_objects.button_sound.play()
        # Si on clique sur n'importe quoi d'autre
        else:
            # On gère tout les cas de paramètres des objets de la classe TextInputBox (se référer au fichier TextInputBox_class.py pour plus d'informations sur ces paramètres)
            if text_input.num_only:
                if event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    if text_input.max_caracteres > 0:
                        if len(text_input.user_text) < text_input.max_caracteres:
                            if not text_input.adaptative_size:
                                if text_input.text_size < text_input.base_size:
                                    text_input.user_text += event.unicode
                            else:
                                text_input.user_text += event.unicode
            else:
                if len(text_input.user_text) < text_input.max_caracteres or text_input.max_caracteres == -1:
                    if not text_input.adaptative_size:
                        if text_input.text_size < text_input.base_size:
                            text_input.user_text += event.unicode
                        else:
                            text_input.user_text += event.unicode
                    else:
                        text_input.user_text += event.unicode
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_BACKSPACE:
            text_input.backspace = False

def changer_raccourci(event : pygame.event.Event, text_input : TextInputBox, raccourcis_dict : dict, indice : int):
    """Change le raccourci donné par un nouveau donné également tout en effectuant les vérifications nécessaires

    Args:
        event (pygame.event.Event): variable des événements pygame
        text_input (TextInputBox): zone de texte à modifier
        raccourcis_dict (dict): dictionnaire des raccourcis concerné
        indice (int): emplacement du raccourci à modifier dans le dictionnaire donné
    """
    if event.type == pygame.KEYDOWN:
        Global_objects.button_sound.play()
        # Si on clique sur supprimer
        if event.key == pygame.K_BACKSPACE:
            text_input.user_text = "Backspace"
            text_input.active = False
            dict_list = list(raccourcis_dict.items())
            dict_list[indice] = (event.unicode, dict_list[indice][1])
            raccourcis_dict = dict(dict_list)
        # Si on clique sur echap
        elif event.key == pygame.K_ESCAPE:
            text_input.user_text = "Esc"
            text_input.active = False
            dict_list = list(raccourcis_dict.items())
            dict_list[indice] = (event.unicode, dict_list[indice][1])
            raccourcis_dict = dict(dict_list)
        # Si on clique sur entrer
        elif event.key == pygame.K_RETURN:
            text_input.user_text = "Enter"
            text_input.active = False
            dict_list = list(raccourcis_dict.items())
            dict_list[indice] = (event.unicode, dict_list[indice][1])
            raccourcis_dict = dict(dict_list)
        # Si on clique sur tab
        elif event.key == pygame.K_TAB:
            text_input.user_text = "Tab"
            text_input.active = False
            dict_list = list(raccourcis_dict.items())
            dict_list[indice] = (event.unicode, dict_list[indice][1])
            raccourcis_dict = dict(dict_list)
        # Si on clique sur n'importe quoi d'autre
        elif event.unicode != "":
            # On gère tout les cas de paramètres des objets de la classe TextInputBox (se référer au fichier TextInputBox_class.py pour plus d'informations sur ces paramètres)
            text_input.user_text = event.unicode
            text_input.active = False
            dict_list = list(raccourcis_dict.items())
            dict_list[indice] = (text_input.user_text, dict_list[indice][1])
            raccourcis_dict = dict(dict_list)

def logs(largeur_actuelle : int, hauteur_actuelle : int, screen : pygame.Surface):
    """Gére l'affichage de logs de débugage ingame

    Args:
        largeur_actuelle (int): Largeur de l'écran (pour width_scale())
        hauteur_actuelle (int): Hauteur de l'écran (pour height_scale())
        screen (pygame.Surface): Ecran sur lequel afficher la fenêtre (écran de l'utilisateur)
    """
    # On gére la transformations des logs
    for i in range(len(Global_objects.logs)):
        try:
            Global_objects.logs[i].texte
        except:
            Global_objects.logs[i] = Logs(str(Global_objects.logs[i]))
    # On check leur timer
    for log in Global_objects.logs:
        log.timer()
    # On redéfinit la variable de comparaison
    Global_objects.previous_logs = Global_objects.logs
    # On gére les positions
    pos_x = width_scale(5, largeur_actuelle)
    pos_y = height_scale(5, hauteur_actuelle)
    # On crée hors de la boucle le style d'écriture
    gui_font = pygame.font.SysFont("Roboto", width_scale(25, largeur_actuelle, True))
    # Pour chaque item dans la liste de logs à partir de la fin on l'affiche
    for log in Global_objects.logs[::-1]:
        text_surf = gui_font.render(log.texte, True, "#FFFFFF")
        screen.blit(text_surf, (pos_x, pos_y))
        """# On affiche également dans la console ce que l'on affiche
        ic(log.texte)"""
        # A la fin on augmente la position y pour afficher le prochain en dessous
        pos_y += height_scale(20, hauteur_actuelle)

class Logs:
    """Classe Logs pour gérer les logs
    """

    def __init__(self, text : str):
        """Initialisation de la classe Logs

        Args:
            text (str): Texte à afficher
        """
        self.texte = text
        self.time_start = time.time()

    def timer(self):
        """Timer pour calculer individuellement le temps de vie des logs
        """
        if self.time_start - time.time() <= -3:
            Global_objects.logs.pop(0)
            del self

def charge_settings(largeur_actuelle : int, hauteur_actuelle : int, screen : pygame.Surface, current_folder : str):
    """Fonction pour charger la sauvegarde locale

    Args:
        current_folder (str): lien du fichier de sauvegarde
    """
    try:
        with open(f"{current_folder}\\settings_save.txt", encoding="utf-8") as file:
            settings = file.readlines()
            # On charge le volume
            music = settings[32].split("\n")
            Global_objects.volume_music = float(music[0])
            Global_objects.music_bar.cursor_width = width_scale(500, largeur_actuelle) + Global_objects.volume_music * (width_scale(700, largeur_actuelle) - width_scale(500, largeur_actuelle))
            # On charge le son
            sound = settings[33].split("\n")
            Global_objects.button_sound_volume = float(sound[0])
            Global_objects.sound_bar.cursor_width = width_scale(500, largeur_actuelle) + Global_objects.button_sound_volume * (width_scale(700, largeur_actuelle) - width_scale(500, largeur_actuelle))
            # On charge les raccourcis clavier
            raccourcis = []
            for elem in settings[:-1]:
                raccourci = elem.split("\n")
                raccourcis.append(raccourci[0])
            Global_objects.raccourcis_mainmenu = {raccourcis[0] if raccourcis[0] != "\\r" else "\r" : Global_objects.playbutton,
                                                  raccourcis[1] if raccourcis[1] != "\\r" else "\r" : Global_objects.settingsbutton,
                                                  raccourcis[2] if raccourcis[2] != "\\r" else "\r" : Global_objects.shopbutton,
                                                  raccourcis[3] if raccourcis[3] != "\\r" else "\r" : Global_objects.accountbutton,
                                                  raccourcis[4] if raccourcis[4] != "\\r" else "\r" : Global_objects.exitbutton}
            
            Global_objects.raccourcis_settingmenu = {raccourcis[5] if raccourcis[5] != "\\r" else "\r" : Global_objects.settingpage1button,
                                                     raccourcis[6] if raccourcis[6] != "\\r" else "\r" : Global_objects.settingpage2button,
                                                     raccourcis[7] if raccourcis[7] != "\\r" else "\r" : Global_objects.settingpage3button,
                                                     raccourcis[8] if raccourcis[8] != "\\r" else "\r" : Global_objects.accountbutton,
                                                     raccourcis[9] if raccourcis[9] != "\\r" else "\r" : Global_objects.backbutton}
            
            Global_objects.raccourcis_accountmenu = {raccourcis[10] if raccourcis[10] != "\\r" else "\r" : Global_objects.accountsettingsbutton,
                                                     raccourcis[11] if raccourcis[11] != "\\r" else "\r" : Global_objects.accountpseudoinput,
                                                     raccourcis[12] if raccourcis[12] != "\\r" else "\r" : Global_objects.accountinformationinput,
                                                     raccourcis[13] if raccourcis[13] != "\\r" else "\r" : Global_objects.deconnexionbutton,
                                                     raccourcis[14] if raccourcis[14] != "\\r" else "\r" : Global_objects.backbutton}
        
            Global_objects.raccourcis_gamemenu = {raccourcis[15] if raccourcis[15] != "\\r" else "\r" : Global_objects.checkbutton,
                                                  raccourcis[16] if raccourcis[16] != "\\r" else "\r" : Global_objects.callbutton,
                                                  raccourcis[17] if raccourcis[17] != "\\r" else "\r" : Global_objects.foldbutton,
                                                  raccourcis[18] if raccourcis[18] != "\\r" else "\r" : Global_objects.raisebutton,
                                                  raccourcis[19] if raccourcis[19] != "\\r" else "\r" : (Global_objects.yesleavebutton, Global_objects.confirmraisebutton),
                                                  raccourcis[20] if raccourcis[20] != "\\r" else "\r" : (Global_objects.noleavebutton, Global_objects.cancelraisebutton),
                                                  raccourcis[21] if raccourcis[21] != "\\r" else "\r" : Global_objects.minus100button,
                                                  raccourcis[22] if raccourcis[22] != "\\r" else "\r" : Global_objects.add100button,
                                                  raccourcis[23] if raccourcis[23] != "\\r" else "\r" : Global_objects.all_inbutton,
                                                  raccourcis[24] if raccourcis[24] != "\\r" else "\r" : Global_objects.sit_upbutton,
                                                  raccourcis[25] if raccourcis[25] != "\\r" else "\r" : Global_objects.leavegamebutton,
                                                  raccourcis[26] if raccourcis[26] != "\\r" else "\r" : Global_objects.gamesettingsbutton}
        
            Global_objects.raccourcis_lobbymenu = {raccourcis[27] if raccourcis[27] != "\\r" else "\r" : Global_objects.previewlobbys.jointablebutton,
                                                   raccourcis[28] if raccourcis[28] != "\\r" else "\r" : Global_objects.createtablebutton,
                                                   raccourcis[29] if raccourcis[29] != "\\r" else "\r" : Global_objects.tablecodeinput,
                                                   raccourcis[30] if raccourcis[30] != "\\r" else "\r" : Global_objects.accountbutton,
                                                   raccourcis[31] if raccourcis[31] != "\\r" else "\r" : Global_objects.backbutton}
    except:
        # On gére le cas où le chargement de la sauvegarde ne fonctionne pas pour quelque raison que ce soit et on rétablit les paramètres par défaut des raccourcis
        Global_objects.raccourcis_mainmenu = {"s" : Global_objects.playbutton,
                                              "q" : Global_objects.settingsbutton,
                                              "d" : Global_objects.shopbutton,
                                              "z" : Global_objects.accountbutton,
                                              "\x1b" : Global_objects.exitbutton}

        Global_objects.raccourcis_settingmenu = {"&" : Global_objects.settingpage1button,
                                                 "é" : Global_objects.settingpage2button,
                                                 '"' : Global_objects.settingpage3button,
                                                 "z" : Global_objects.accountbutton,
                                                 "\x1b" : Global_objects.backbutton}
        
        Global_objects.raccourcis_accountmenu = {"a" : Global_objects.accountsettingsbutton,
                                                 "q" : Global_objects.accountpseudoinput,
                                                 "s" : Global_objects.accountinformationinput,
                                                 "w" : Global_objects.deconnexionbutton,
                                                 "\x1b" : Global_objects.backbutton}
        
        Global_objects.raccourcis_gamemenu = {"w" : Global_objects.checkbutton,
                                              "x" : Global_objects.callbutton,
                                              "c" : Global_objects.foldbutton,
                                              "v" : Global_objects.raisebutton,
                                              "\r" : (Global_objects.yesleavebutton, Global_objects.confirmraisebutton),
                                              "\x08" : (Global_objects.noleavebutton, Global_objects.cancelraisebutton),
                                              "," : Global_objects.minus100button,
                                              ";" : Global_objects.add100button,
                                              ":" : Global_objects.all_inbutton,
                                              "b" : Global_objects.sit_upbutton,
                                              "n" : Global_objects.leavegamebutton,
                                              "\x1b" : Global_objects.gamesettingsbutton}
        
        Global_objects.raccourcis_lobbymenu = {"\r" : Global_objects.previewlobbys.jointablebutton,
                                               "a" : Global_objects.createtablebutton,
                                               "w" : Global_objects.tablecodeinput,
                                               "z" : Global_objects.accountbutton,
                                               "\x1b" : Global_objects.backbutton}

def sauvegarder_settings():
    with open(f"{__file__[:-23]}\\settings_save.txt", "w", encoding="utf-8") as file:
        for raccourci in Global_objects.raccourcis_mainmenu.keys():
            file.write(f"{raccourci}\n") if raccourci != "\r" else file.write(r"\r"+"\n")
        for raccourci in Global_objects.raccourcis_settingmenu.keys():
            file.write(f"{raccourci}\n") if raccourci != "\r" else file.write(r"\r"+"\n")
        for raccourci in Global_objects.raccourcis_accountmenu.keys():
            file.write(f"{raccourci}\n") if raccourci != "\r" else file.write(r"\r"+"\n")
        for raccourci in Global_objects.raccourcis_gamemenu.keys():
            file.write(f"{raccourci}\n") if raccourci != "\r" else file.write(r"\r"+"\n")
        for raccourci in Global_objects.raccourcis_lobbymenu.keys():
            file.write(f"{raccourci}\n") if raccourci != "\r" else file.write(r"\r"+"\n")
        file.write(f"{Global_objects.volume_music}\n")
        file.write(f"{Global_objects.button_sound_volume}\n")