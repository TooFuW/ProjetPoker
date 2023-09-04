# Check player's clicks


import pygame
import sys
import Global_objects
from network import *
import time


# Permet de savoir si les paramètres en jeu sont actifs pour bloquer les interactions avec le reste lorsque le menu des paramètres est actif
Global_objects.game_settings_enabled = False


# La fonction check_click est appellée à chaque fois que l'utilisateur clique sur un bouton
def check_click(Button):
    """Check_click est appellée à chaque fois que l'utilisateur clique sur un bouton et agit en fonction de l'attribut "fonction" du bouton.

    Args:
        Button (Button class object): Boutton sur lequel l'utilisateur a cliqué et qui va faire l'action correspondante
    """
    match Button.fonction:
        # Lorsque le bouton PLAY est cliqué
        case "play":
            try:
                ask_lobbys(Global_objects.client_socket)
            except:
                pass
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
                try:
                    lobby_id = int(Global_objects.game_state.table_selected[-1])
                    Global_objects.previewlobbys.players = ask_sits_infos(Global_objects.client_socket,lobby_id)
                    print(Global_objects.previewlobbys.players)
                except:
                    pass
                time.sleep(0.2)
        # Lorsque le bouton JOIN est cliqué pour rejoindre la table sélectionnée et transmettre les infos nécessaires
        case "join table":
            try:
                lobby_id = int(Global_objects.game_state.table_selected[-1])
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
                Global_objects.game_state.table_selected = None
                Global_objects.game_state.back_pile = []
                Global_objects.game_state.state = "Game Menu"
                Global_objects.is_selecting_sit[0] = True
                print("JOIN TABLE")
            except:
                Global_objects.game_state.error[0] = True
                Global_objects.game_state.error[1] = time.time()
        # Lorsque le bouton CREATE TABLE est cliqué pour passer à la page de création de table
        case "create table":
            Global_objects.game_state.back_pile.append(Global_objects.game_state.state)
            Global_objects.game_state.state = "Create Menu"
        # Lorsque le bouton REFRESH est cliqué  pour réactualiser les tables affichés dans l'objet serverscrollbox
        case "refresh":
            ask_lobbys(Global_objects.client_socket)
            Global_objects.serverscrollbox.scroll_pos = 0
            Global_objects.game_state.table_selected = None
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
            Global_objects.game_state.back_pile.append(Global_objects.game_state.state)
            Global_objects.game_state.state = "Setting Menu"
            Global_objects.game_state.setting_page = 1
            Global_objects.settingpage1button.initial_bottom_color = "#475F77"
            Global_objects.settingpage1button.hovering_bottom_color = "#D74B4B"
            Global_objects.settingpage2button.initial_bottom_color = "#354B5E"
            Global_objects.settingpage3button.initial_bottom_color = "#354B5E"
        # Lorsque le bouton pour quitter la partie cliqué
        case "leave game":
            Global_objects.game_state.confirmation = True
            Global_objects.is_selecting_sit = [False, -1]
        # Lorsque le joueur confirme qu'il veut quitter
        case "yes":
            Global_objects.game_state.state = "Main Menu"
            go_main(Global_objects.client_socket)
            Global_objects.game_state.confirmation = False
        # Lorsque le joueur ne confirme pas qu'il veut quitter
        case "no":
            Global_objects.game_state.confirmation = False
        # Lorsqu'un bouton pour s'asseoir est cliqué
        case "sit 1":
            Global_objects.is_selecting_sit[1] = 0
            sit_down(Global_objects.client_socket, 0)
            print("@@@@@@@@@@@@")
            Global_objects.is_selecting_sit = [False, -1]
        case "sit 2":
            Global_objects.is_selecting_sit[1] = 1
            sit_down(Global_objects.client_socket, 1)
            print("@@@@@@@@@@@@")
            Global_objects.is_selecting_sit = [False, -1]
        case "sit 3":
            Global_objects.is_selecting_sit[1] = 2
            sit_down(Global_objects.client_socket, 2)
            print("@@@@@@@@@@@@")
            Global_objects.is_selecting_sit = [False, -1]
        case "sit 4":
            Global_objects.is_selecting_sit[1] = 3
            sit_down(Global_objects.client_socket, 3)
            print("@@@@@@@@@@@@")
            Global_objects.is_selecting_sit = [False, -1]
        case "sit 5":
            Global_objects.is_selecting_sit[1] = 4
            sit_down(Global_objects.client_socket, 4)
            print("@@@@@@@@@@@@")
            Global_objects.is_selecting_sit = [False, -1]
        case "sit 6":
            Global_objects.is_selecting_sit[1] = 5
            sit_down(Global_objects.client_socket, 5)
            print("@@@@@@@@@@@@")
            Global_objects.is_selecting_sit = [False, -1]
        case "sit 7":
            Global_objects.is_selecting_sit[1] = 6
            sit_down(Global_objects.client_socket, 6)
            print("@@@@@@@@@@@@")
            Global_objects.is_selecting_sit = [False, -1]
        case "sit 8":
            Global_objects.is_selecting_sit[1] = 7
            sit_down(Global_objects.client_socket, 7)
            print("@@@@@@@@@@@@")
            Global_objects.is_selecting_sit = [False, -1]
        case "sit 9":
            Global_objects.is_selecting_sit[1] = 8
            sit_down(Global_objects.client_socket, 8)
            print("@@@@@@@@@@@@")
            Global_objects.is_selecting_sit = [False, -1]
        case "sit 10":
            Global_objects.is_selecting_sit[1] = 9
            sit_down(Global_objects.client_socket, 9)
            print("@@@@@@@@@@@@")
            Global_objects.is_selecting_sit = [False, -1]