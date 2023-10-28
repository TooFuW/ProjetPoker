"""Document contenant des fonctions pratiques afin d'éviter des répétitions dans HUD_State_class.py et réduire le nombre de lignes"""


import pygame
from Screen_adaptation import *
import Global_objects
from TextInputBox_class import *
import time


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
        event (pygame.event.Event): _description_
        text_input (TextInputBox): _description_
    """
    if event.type == pygame.KEYDOWN:
        # Si on clique sur supprimer
        if event.key == pygame.K_BACKSPACE:
            text_input.backspace = True
        # Si on clique sur entrer
        elif event.key == pygame.K_RETURN:
            text_input.active = False
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