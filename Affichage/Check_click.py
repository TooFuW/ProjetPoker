# Check player's clicks


import pygame
import sys
import Global_objects
from HUD_State_class import *
from network import *


# Permet de savoir si les paramètres en jeu sont actifs pour bloquer les interactions avec le reste lorsque le menu des paramètres est actif
Global_objects.game_settings_enabled = False


# La fonction check_click est appellée à chaque fois que l'utilisateur clique sur un bouton
def check_click(Button):
    """Check_click est appellée à chaque fois que l'utilisateur clique sur un bouton et agit en fonction de l'attribut "fonction" du bouton.

    Args:
        Button (Button class object): Boutton sur lequel l'utilisateur a cliqué et qui va faire l'acion correspondante
    """
    # Dans le cas où le menu des paramètres en jeu est activé, on désactive l'utilisation des autres boutons en arrière-plan
    if Global_objects.game_settings_enabled is False:
        match Button.fonction:
            # Lorsque le bouton PLAY est cliqué
            case "play":
                ask_lobbys(Global_objects.client_socket)
                Global_objects.game_state.back_pile.append(Global_objects.game_state.state)
                Global_objects.game_state.state = "Lobby Menu"
            # Lorsque le bouton SETTINGS est cliqué
            case "settings":
                Global_objects.game_state.back_pile.append(Global_objects.game_state.state)
                Global_objects.game_state.state = "Setting Menu"
                Global_objects.game_state.setting_page = 1
                Global_objects.settingpage1button.initial_bottom_color = "#475F77"
                Global_objects.settingpage1button.hovering_bottom_color = "#D74B4B"
                Global_objects.settingpage2button.initial_bottom_color = "#354B5E"
                Global_objects.settingpage3button.initial_bottom_color = "#354B5E"
            # Lorsque le bouton ACCOUNT est cliqué
            case "account":
                Global_objects.game_state.back_pile.append(Global_objects.game_state.state)
                Global_objects.game_state.state = "Account Menu"
                if Global_objects.accountsettingsbutton.account_modifiable == True:
                    Global_objects.accountpseudoinput.interactible = False
                    Global_objects.accountinformationinput.interactible = False
                    Global_objects.accountpseudoinput.color_passive = "#475F77"
                    Global_objects.accountinformationinput.color_passive = "#475F77"
                    Global_objects.accountsettingsbutton.initial_top_color = "#D74B4B"
                    Global_objects.accountsettingsbutton.bottom_color = "#D74B4B"
                    Global_objects.accountsettingsbutton.hovering_color = "#D74B4B"
                    Global_objects.accountsettingsbutton.account_modifiable = False
            # Lorsque le bouton EXIT est cliqué
            case "exit":
                pygame.quit()
                sys.exit()
            # Lorsque le bouton HISTORY est cliqué
            case "history":
                Global_objects.game_state.back_pile.append(Global_objects.game_state.state)
                Global_objects.game_state.state = "History Menu"
            # Lorsque le bouton PAGE 1 dans SETTINGS est cliqué
            case "setting page 1":
                Global_objects.game_state.setting_page = 1
                Global_objects.settingpage1button.initial_bottom_color = "#475F77"
                Global_objects.settingpage1button.hovering_bottom_color = "#D74B4B"
                Global_objects.settingpage2button.initial_bottom_color = "#354B5E"
                Global_objects.settingpage3button.initial_bottom_color = "#354B5E"
            # Lorsque le bouton PAGE 2 dans SETTINGS est cliqué
            case "setting page 2":
                Global_objects.game_state.setting_page = 2
                Global_objects.settingpage1button.initial_bottom_color = "#354B5E"
                Global_objects.settingpage2button.initial_bottom_color = "#475F77"
                Global_objects.settingpage2button.hovering_bottom_color = "#D74B4B"
                Global_objects.settingpage3button.initial_bottom_color = "#354B5E"
            # Lorsque le bouton PAGE 3 dans SETTINGS est cliqué
            case "setting page 3":
                Global_objects.game_state.setting_page = 3
                Global_objects.settingpage1button.initial_bottom_color = "#354B5E"
                Global_objects.settingpage2button.initial_bottom_color = "#354B5E"
                Global_objects.settingpage3button.initial_bottom_color = "#475F77"
                Global_objects.settingpage3button.hovering_bottom_color = "#D74B4B"
            # Lorsque le bouton des paramètres dans ACCOUNT est cliqué
            case "account settings":
                if Global_objects.accountsettingsbutton.account_modifiable == True:
                    Global_objects.accountpseudoinput.interactible = False
                    Global_objects.accountinformationinput.interactible = False
                    Global_objects.accountpseudoinput.color_passive = "#475F77"
                    Global_objects.accountinformationinput.color_passive = "#475F77"
                    Global_objects.accountsettingsbutton.initial_top_color = "#D74B4B"
                    Global_objects.accountsettingsbutton.hovering_color = "#D74B4B"
                    Global_objects.accountsettingsbutton.account_modifiable = False
                else:
                    Global_objects.accountpseudoinput.interactible = True
                    Global_objects.accountinformationinput.interactible = True
                    Global_objects.accountpseudoinput.color_passive = "#475F90"
                    Global_objects.accountinformationinput.color_passive = "#475F90"
                    Global_objects.accountsettingsbutton.initial_top_color = "#00FF00"
                    Global_objects.accountsettingsbutton.hovering_color = "#00FF00"
                    Global_objects.accountsettingsbutton.account_modifiable = True
            # Lorsqu'un bouton de serveur est cliqué
            case "server":
                if Global_objects.game_state.state == "Lobby Menu":
                    Global_objects.game_state.server_test = Button.text
                    Global_objects.game_state.table_selected = Button.text.split("          ")
                    ask_sits_infos(Global_objects.client_socket)
            # Lorsque le bouton JOIN est cliqué pour rejoindre la table sélectionnée
            case "join table":
                Global_objects.game_state.back_pile = ["Main Menu"]
                Global_objects.game_state.state = "Game Menu"
                Global_objects.game_state.table_selected = None
            # Lorsque le bouton CREATE TABLE est cliqué pour passer à la page de création de table
            case "create table":
                Global_objects.game_state.back_pile.append(Global_objects.game_state.state)
                Global_objects.game_state.state = "Create Menu"
            # Lorsque le bouton REFRESH est cliqué  pour réactualiser les tables affichés dans l'objet serverscrollbox
            case "refresh":
                ask_lobbys(Global_objects.client_socket)
                Global_objects.serverscrollbox.scroll_pos = 0
    match Button.fonction:
        # Lorsque le bouton BACK (fléche retour) est cliqué
        case "back":
            Global_objects.game_state.setting_page = 1
            Global_objects.settingpage1button.initial_bottom_color = "#475F77"
            Global_objects.settingpage1button.hovering_bottom_color = "#D74B4B"
            Global_objects.settingpage2button.initial_bottom_color = "#354B5E"
            Global_objects.settingpage3button.initial_bottom_color = "#354B5E"
            Global_objects.game_state.gamesettings = False
            Global_objects.game_state.state = Global_objects.game_state.back_pile.pop()
            Global_objects.game_settings_enabled = False
            Global_objects.game_state.table_selected = None
        # Lorsque le bouton des paramètres en jeu est cliqué
        case "game settings":
            if Global_objects.game_state.gamesettings == False:
                Global_objects.game_state.gamesettings = True
                Global_objects.game_settings_enabled = True
            else:
                Global_objects.game_state.gamesettings = False
                Global_objects.game_settings_enabled = False