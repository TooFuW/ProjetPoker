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
    # On gére les positions
    pos_x = width_scale(5, largeur_actuelle)
    pos_y = height_scale(5, hauteur_actuelle)
    # On crée hors de la boucle le style d'écriture
    gui_font = pygame.font.SysFont("Roboto", width_scale(25, largeur_actuelle, True))
    # Pour chaque item dans la liste de logs à partir de la fin on l'affiche
    for log in Global_objects.logs[::-1]:
        text_surf = gui_font.render(log.texte, True, "#FFFFFF")
        screen.blit(text_surf, (pos_x, pos_y))
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