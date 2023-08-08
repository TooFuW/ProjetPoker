# Check player's clicks


import pygame
import sys
from Global_objects import *


def check_click(Button):
    if Button.fonction == "play":
        Global_game_state.back_pile.append(Global_game_state.state)
        Global_game_state.state = "Lobby Menu"
    elif Button.fonction == "settings":
        Global_game_state.back_pile.append(Global_game_state.state)
        Global_game_state.state = "Setting Menu"
        Global_game_state.setting_page = 1
    elif Button.fonction == "account":
        Global_game_state.back_pile.append(Global_game_state.state)
        Global_game_state.state = "Account Menu"
    elif Button.fonction == "exit":
        pygame.quit()
        sys.exit()
    elif Button.fonction == "back":
        if Global_game_state.back_pile[-1] == "Setting Menu":
            Global_game_state.setting_page = 1
        Global_game_state.state = Global_game_state.back_pile.pop()
    elif Button.fonction == "history":
        Global_game_state.back_pile.append(Global_game_state.state)
        Global_game_state.state = "History Menu"
    elif Button.fonction == "setting page 1":
        Global_game_state.setting_page = 1
    elif Button.fonction == "setting page 2":
        Global_game_state.setting_page = 2
    elif Button.fonction == "setting page 3":
        Global_game_state.setting_page = 3
    elif Button.fonction == "account settings":
        if Global_accountsettingsbutton.account_modifiable == True:
            Global_accountpseudoinput.interactible = False
            Global_accountinformationinput.interactible = False
            Global_accountpseudoinput.color_passive = "#475F77"
            Global_accountinformationinput.color_passive = "#475F77"
            Global_accountsettingsbutton.initial_top_color = "#D74B4B"
            Global_accountsettingsbutton.bottom_color = "#D74B4B"
            Global_accountsettingsbutton.hovering_color = "#D74B4B"
            Global_accountsettingsbutton.account_modifiable = False
        else:
            Global_accountpseudoinput.interactible = True
            Global_accountinformationinput.interactible = True
            Global_accountpseudoinput.color_passive = "#475F90"
            Global_accountinformationinput.color_passive = "#475F90"
            Global_accountsettingsbutton.initial_top_color = "#00FF00"
            Global_accountsettingsbutton.bottom_color = "#00FF00"
            Global_accountsettingsbutton.hovering_color = "#00FF00"
            Global_accountsettingsbutton.account_modifiable = True