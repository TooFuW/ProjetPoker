# Check player's clicks


import pygame
import sys
import Global_objects
from HUD_State_class import *


# La fonction check_click est appellée à chaque fois que l'utilisateur clique sur un bouton
def check_click(Button):
    """Check_click est appellée à chaque fois que l'utilisateur clique sur un bouton et agit en fonction de l'attribut "fonction" du bouton.

    Args:
        Button (Non défini): Boutton sur lequel l'utilisateur a cliqué et qui va faire l'acion correspondante
    """
    if Button.fonction == "play":
        Global_objects.game_state.back_pile.append(Global_objects.game_state.state)
        Global_objects.game_state.state = "Lobby Menu"
    elif Button.fonction == "settings":
        Global_objects.game_state.back_pile.append(Global_objects.game_state.state)
        Global_objects.game_state.state = "Setting Menu"
        Global_objects.game_state.setting_page = 1
    elif Button.fonction == "account":
        Global_objects.game_state.back_pile.append(Global_objects.game_state.state)
        Global_objects.game_state.state = "Account Menu"
    elif Button.fonction == "exit":
        pygame.quit()
        sys.exit()
    elif Button.fonction == "back":
        if Global_objects.game_state.back_pile[-1] == "Setting Menu":
            Global_objects.game_state.setting_page = 1
        Global_objects.game_state.state = Global_objects.game_state.back_pile.pop()
    elif Button.fonction == "history":
        Global_objects.game_state.back_pile.append(Global_objects.game_state.state)
        Global_objects.game_state.state = "History Menu"
    elif Button.fonction == "setting page 1":
        Global_objects.game_state.setting_page = 1
    elif Button.fonction == "setting page 2":
        Global_objects.game_state.setting_page = 2
    elif Button.fonction == "setting page 3":
        Global_objects.game_state.setting_page = 3
    elif Button.fonction == "account settings":
        if Global_objects.accountsettingsbutton.account_modifiable == True:
            Global_objects.accountpseudoinput.interactible = False
            Global_objects.accountinformationinput.interactible = False
            Global_objects.accountpseudoinput.color_passive = "#475F77"
            Global_objects.accountinformationinput.color_passive = "#475F77"
            Global_objects.accountsettingsbutton.initial_top_color = "#D74B4B"
            Global_objects.accountsettingsbutton.bottom_color = "#D74B4B"
            Global_objects.accountsettingsbutton.hovering_color = "#D74B4B"
            Global_objects.accountsettingsbutton.account_modifiable = False
        else:
            Global_objects.accountpseudoinput.interactible = True
            Global_objects.accountinformationinput.interactible = True
            Global_objects.accountpseudoinput.color_passive = "#475F90"
            Global_objects.accountinformationinput.color_passive = "#475F90"
            Global_objects.accountsettingsbutton.initial_top_color = "#00FF00"
            Global_objects.accountsettingsbutton.bottom_color = "#00FF00"
            Global_objects.accountsettingsbutton.hovering_color = "#00FF00"
            Global_objects.accountsettingsbutton.account_modifiable = True
    elif Button.fonction == "server":
        Global_objects.game_state.back_pile = ["Main Menu"]
        Global_objects.game_state.state = "Game Menu"
        Global_objects.game_state.server_test = Button.text