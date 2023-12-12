"""Document contenant la fonction check_click qui fait les actions liées aux interactions de l'utilisateur"""


import pygame
import sys
import Global_objects
from network import *
import time
from Screen_adaptation import *
from random import randint
from Fonctions_pratiques import *


# La fonction check_click est appellée à chaque fois que l'utilisateur clique sur un bouton
def check_click(Button):
    """Check_click est appellée à chaque fois que l'utilisateur clique sur un bouton et agit en fonction de l'attribut "fonction" du bouton.

    Args:
        Button (Button class object): Boutton sur lequel l'utilisateur a cliqué et qui va faire l'action correspondante
    """
    Global_objects.button_sound.play()
    if Global_objects.buttons_interactibles:
        match Button.fonction:
            # Lorsque le bouton PLAY est cliqué
            case "play":
                try:
                    ask_lobbys(Global_objects.client_socket)
                except:
                    pass
                Global_objects.game_state.back_pile.append(Global_objects.game_state.state)
                Global_objects.game_state.state = "Lobby Menu"
                Global_objects.auto_arrived_sits = None
            # Lorsque le bouton SETTINGS est cliqué
            case "settings":
                Global_objects.game_state.back_pile.append(Global_objects.game_state.state)
                Global_objects.game_state.state = "Setting Menu"
                Global_objects.game_state.setting_page = 1
            # Lorsque le bouton ACCOUNT est cliqué
            case "account":
                Global_objects.game_state.back_pile.append(Global_objects.game_state.state)
                Global_objects.game_state.state = "Account Menu"
                if Global_objects.accountsettingsbutton.account_modifiable:
                    Global_objects.accountpseudoinput.interactible = False
                    Global_objects.accountinformationinput.interactible = False
                    Global_objects.accountpseudoinput.color_passive = "#888888"
                    Global_objects.accountinformationinput.color_passive = "#888888"
                    Global_objects.accountsettingsbutton.initial_color = (0, 255, 0, 180)
                    Global_objects.accountsettingsbutton.hovering_color = (0, 255, 0, 200)
                    Global_objects.accountsettingsbutton.clicking_color = (0, 255, 0, 220)
                    Global_objects.accountsettingsbutton.account_modifiable = False
            # Lorsque le bouton EXIT est cliqué
            case "exit":
                pygame.quit()
                sys.exit()
            # Lorsque le bouton SHOP est cliqué
            case "shop":
                Global_objects.game_state.back_pile.append(Global_objects.game_state.state)
                Global_objects.game_state.state = "Shop Menu"
            # Lorsque le bouton PAGE 1 dans SETTINGS est cliqué
            case "setting page 1":
                Global_objects.game_state.setting_page = 1
            # Lorsque le bouton PAGE 2 dans SETTINGS est cliqué
            case "setting page 2":
                Global_objects.game_state.setting_page = 2
            # Lorsque le bouton PAGE 3 dans SETTINGS est cliqué
            case "setting page 3":
                Global_objects.game_state.setting_page = 3
            # Lorsque le bouton des paramètres dans ACCOUNT est cliqué
            case "account settings":
                if Global_objects.accountsettingsbutton.account_modifiable:
                    Global_objects.accountpseudoinput.interactible = False
                    Global_objects.accountinformationinput.interactible = False
                    Global_objects.accountpseudoinput.color_passive = "#888888"
                    Global_objects.accountinformationinput.color_passive = "#888888"
                    Global_objects.accountsettingsbutton.initial_color = (255, 0, 0, 180)
                    Global_objects.accountsettingsbutton.hovering_color = (255, 0, 0, 200)
                    Global_objects.accountsettingsbutton.clicking_color = (255, 0, 0, 220)
                    Global_objects.accountsettingsbutton.account_modifiable = False
                else:
                    Global_objects.accountpseudoinput.interactible = True
                    Global_objects.accountinformationinput.interactible = True
                    Global_objects.accountpseudoinput.color_passive = "#666666"
                    Global_objects.accountinformationinput.color_passive = "#666666"
                    Global_objects.accountsettingsbutton.initial_color = (0, 255, 0, 180)
                    Global_objects.accountsettingsbutton.hovering_color = (0, 255, 0, 200)
                    Global_objects.accountsettingsbutton.clicking_color = (0, 255, 0, 220)
                    Global_objects.accountsettingsbutton.account_modifiable = True
            # Lorsqu'un bouton de serveur est cliqué
            case "server":
                Global_objects.game_state.server_test = Button.text
                Global_objects.table_selected = Button.text.split(" "*width_scale(35, Button.largeur_actuelle, True))
                lobby_id = int(Global_objects.table_selected[-1])
                try:
                    Global_objects.previewlobbys.players = ask_sits_infos(Global_objects.client_socket,lobby_id)
                except:
                    pass
                #time.sleep(0.1)
            # Lorsque le bouton JOIN est cliqué pour rejoindre la table sélectionnée et transmettre les infos nécessaires
            case "join table":
                try:
                    # On indique au serveur qu'on veut rejoindre tel lobby
                    lobby_id = int(Global_objects.table_selected[-1])
                    join_lobby(Global_objects.client_socket,lobby_id)
                    # On attribue les bons sièges avec les bons joueurs
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
                    Global_objects.auto_arrived_sits = ask_sits_infos(Global_objects.client_socket,lobby_id)
                    Global_objects.game_state.back_pile = []
                    # On remet l'écran de chargement à zéro
                    Global_objects.game_state.loading_text = "LOADING"
                    Global_objects.game_state.loading_text_timer = time.time()
                    p1 = randint(1, 35)
                    p2 = randint(p1+1, 70)
                    p3 = randint(p2+1, 98)
                    Global_objects.game_state.chargement_pourcent = [0, p1, p2, p3, 99]
                    Global_objects.game_state.chargement_indice = 0
                    Global_objects.game_state.chargement_valeur = 0
                    Global_objects.game_state.chargement_pause = time.time()
                    Global_objects.game_state.chargement_temps_pause = -1
                    Global_objects.previewchargement.players = Global_objects.previewlobbys.players
                    Global_objects.game_state.state = "Chargement"
                    Global_objects.game_state.chargement_next_state = "Game Menu"
                    # On définit toutes les variables pour gérer la partie
                    Global_objects.is_selecting_sit[0] = True
                    Global_objects.game_started = False
                    Global_objects.pot = Global_objects.table_selected[3]
                except:
                    # Sinon on déclenche l'erreur
                    Global_objects.game_state.error[0] = True
                    Global_objects.game_state.error[1] = time.time()
            # Lorsque le bouton CREATE TABLE est cliqué pour passer à la page de création de table
            case "create table":
                Global_objects.game_state.back_pile.append(Global_objects.game_state.state)
                Global_objects.game_state.state = "Create Menu"
            # Lorsque le bouton REFRESH est cliqué  pour réactualiser les tables affichés dans l'objet serverscrollbox
            case "refresh":
                try:
                    ask_lobbys(Global_objects.client_socket)
                except:
                    pass
                Global_objects.serverscrollbox.scroll_pos = 0
                Global_objects.table_selected = None
            # Lorsque le bouton BACK (fléche retour) est cliqué
            case "back":
                Global_objects.game_state.setting_page = 1
                Global_objects.game_state.state = Global_objects.game_state.back_pile.pop()
                Global_objects.table_selected = None
            # Lorsque le bouton des paramètres en jeu est cliqué
            case "game settings":
                Global_objects.game_state.back_pile.append(Global_objects.game_state.state)
                Global_objects.game_state.state = "Setting Menu"
                Global_objects.game_state.setting_page = 1
            # Lorsque le bouton pour quitter la partie cliqué
            case "leave game":
                Global_objects.game_state.confirmation = True
                Global_objects.buttons_interactibles = False
            # Lorsqu'un bouton pour s'asseoir est cliqué
            case "sit 1":
                Global_objects.is_selecting_sit[1] = 0
                sit_down(Global_objects.client_socket, 0)
                Global_objects.is_selecting_sit = [False, -1]
                Global_objects.client_actuel = 1
            case "sit 2":
                Global_objects.is_selecting_sit[1] = 1
                sit_down(Global_objects.client_socket, 1)
                Global_objects.is_selecting_sit = [False, -1]
                Global_objects.client_actuel = 2
            case "sit 3":
                Global_objects.is_selecting_sit[1] = 2
                sit_down(Global_objects.client_socket, 2)
                Global_objects.is_selecting_sit = [False, -1]
                Global_objects.client_actuel = 3
            case "sit 4":
                Global_objects.is_selecting_sit[1] = 3
                sit_down(Global_objects.client_socket, 3)
                Global_objects.is_selecting_sit = [False, -1]
                Global_objects.client_actuel = 4
            case "sit 5":
                Global_objects.is_selecting_sit[1] = 4
                sit_down(Global_objects.client_socket, 4)
                Global_objects.is_selecting_sit = [False, -1]
                Global_objects.client_actuel = 5
            case "sit 6":
                Global_objects.is_selecting_sit[1] = 5
                sit_down(Global_objects.client_socket, 5)
                Global_objects.is_selecting_sit = [False, -1]
                Global_objects.client_actuel = 6
            case "sit 7":
                Global_objects.is_selecting_sit[1] = 6
                sit_down(Global_objects.client_socket, 6)
                Global_objects.is_selecting_sit = [False, -1]
                Global_objects.client_actuel = 7
            case "sit 8":
                Global_objects.is_selecting_sit[1] = 7
                sit_down(Global_objects.client_socket, 7)
                Global_objects.is_selecting_sit = [False, -1]
                Global_objects.client_actuel = 8
            case "sit 9":
                Global_objects.is_selecting_sit[1] = 8
                sit_down(Global_objects.client_socket, 8)
                Global_objects.is_selecting_sit = [False, -1]
                Global_objects.client_actuel = 9
            case "sit 10":
                Global_objects.is_selecting_sit[1] = 9
                sit_down(Global_objects.client_socket, 9)
                Global_objects.is_selecting_sit = [False, -1]
                Global_objects.client_actuel = 10
            # Lorsque le bouton pour se lever est cliqué
            case "sit up":
                sit_up(Global_objects.client_socket)
                Global_objects.is_selecting_sit[0] = True
                Global_objects.client_actuel = 0
                for sit in Global_objects.all_sits:
                    sit.pos_card1_x_arrive = sit.x + width_scale(40, sit.largeur_actuelle)
                    sit.pos_card1_y_arrive = sit.y - height_scale(100, sit.hauteur_actuelle)
                    sit.pos_card2_x_arrive = sit.x + width_scale(140, sit.largeur_actuelle)
                    sit.pos_card2_y_arrive = sit.y - height_scale(100, sit.hauteur_actuelle)
                    sit.pos_card1_x_actuel = width_scale(930, sit.largeur_actuelle)
                    sit.pos_card1_y_actuel = height_scale(490, sit.hauteur_actuelle)
                    sit.pos_card2_x_actuel = width_scale(930, sit.largeur_actuelle)
                    sit.pos_card2_y_actuel = height_scale(490, sit.hauteur_actuelle)
                    sit.pas_card1_x = (sit.pos_card1_x_arrive - width_scale(930, sit.largeur_actuelle))/20
                    sit.pas_card1_y = (sit.pos_card1_y_arrive - height_scale(490, sit.hauteur_actuelle))/20
                    sit.pas_card2_x = (sit.pos_card2_x_arrive - width_scale(930, sit.largeur_actuelle))/20
                    sit.pas_card2_y = (sit.pos_card2_y_arrive - height_scale(490, sit.hauteur_actuelle))/20
            # Lorsque l'on clique sur le bouton check
            # appelle la fonction send_action de network avec l'action dans un tuple (action,montant)
            case "check":
                # On renvoit une information sous la forme "my_play=action,montant"
                print("my_play=check")
                send_action(Global_objects.client_socket,("bet",0))
                Global_objects.game_state.timer[0] = 0
            # Lorsque l'on clique sur le bouton call
            case "call":
                # On renvoit une information sous la forme "my_play=action,montant"
                print("my_play=call")
                send_action(Global_objects.client_socket,("bet",Global_objects.bet))
                Global_objects.game_state.timer[0] = 0
            # Lorsque l'on clique sur le bouton fold
            case "fold":
                # On renvoit une information sous la forme "my_play=action,montant"
                print("my_play=fold")
                send_action(Global_objects.client_socket,("fold",0))
                Global_objects.game_state.timer[0] = 0
            # Lorsque l'on clique sur le bouton raise
            case "raise":
                # On renvoit une information sous la forme "my_play=action,montant"
                Global_objects.is_raising = True
                Global_objects.buttons_interactibles = False
                print("my_play=raise")
            # Lorsque l'on clique sur le bouton SAVE
            case "save settings":
                sauvegarder_settings()
    # Cas des boutons non affectés par Global_objects.buttons_interactibles
    match Button.fonction:
        # Lorsque le joueur confirme qu'il veut quitter
        case "yes_leave":
            go_main(Global_objects.client_socket)
            Global_objects.client_actuel = 0
            Global_objects.game_state.state = "Main Menu"
            Global_objects.game_state.confirmation = False
            Global_objects.is_selecting_sit = [False, -1]
            Global_objects.buttons_interactibles = True
            Global_objects.table_selected = None
            Global_objects.auto_arrived_sits = None
            for sit in Global_objects.all_sits:
                sit.pos_card1_x_arrive = sit.x + width_scale(40, sit.largeur_actuelle)
                sit.pos_card1_y_arrive = sit.y - height_scale(100, sit.hauteur_actuelle)
                sit.pos_card2_x_arrive = sit.x + width_scale(140, sit.largeur_actuelle)
                sit.pos_card2_y_arrive = sit.y - height_scale(100, sit.hauteur_actuelle)
                sit.pos_card1_x_actuel = width_scale(930, sit.largeur_actuelle)
                sit.pos_card1_y_actuel = height_scale(490, sit.hauteur_actuelle)
                sit.pos_card2_x_actuel = width_scale(930, sit.largeur_actuelle)
                sit.pos_card2_y_actuel = height_scale(490, sit.hauteur_actuelle)
                sit.pas_card1_x = (sit.pos_card1_x_arrive - width_scale(930, sit.largeur_actuelle))/20
                sit.pas_card1_y = (sit.pos_card1_y_arrive - height_scale(490, sit.hauteur_actuelle))/20
                sit.pas_card2_x = (sit.pos_card2_x_arrive - width_scale(930, sit.largeur_actuelle))/20
                sit.pas_card2_y = (sit.pos_card2_y_arrive - height_scale(490, sit.hauteur_actuelle))/20
        # Lorsque le joueur ne confirme pas qu'il veut quitter
        case "no_leave":
            Global_objects.game_state.confirmation = False
            Global_objects.buttons_interactibles = True
        # Lorsque l'on clique sur le bouton all_in
        case "all_in":
            Global_objects.raise_bar.cursor_width = 1530
        # Lorsque l'on clique sur le bouton add_100
        case "add_100":
            nouvelle_valeur = (((Global_objects.connected_account[2]/100)*Global_objects.raised_amount)*100) + 100 if (((Global_objects.connected_account[2]/100)*Global_objects.raised_amount)*100) + 100 <= Global_objects.connected_account[2] else Global_objects.connected_account[2]
            Global_objects.raise_bar.cursor_width = width_scale(400, Button.largeur_actuelle) + (nouvelle_valeur / Global_objects.connected_account[2]) * (width_scale(1530, Button.largeur_actuelle) - width_scale(400, Button.largeur_actuelle))
        # Lorsque l'on clique sur le bouton minus_100
        case "minus_100":
            nouvelle_valeur = (((Global_objects.connected_account[2]/100)*Global_objects.raised_amount)*100) - 100 if (((Global_objects.connected_account[2]/100)*Global_objects.raised_amount)*100) - 100 >= 0 else 0
            Global_objects.raise_bar.cursor_width = width_scale(400, Button.largeur_actuelle) + (nouvelle_valeur / Global_objects.connected_account[2]) * (width_scale(1530, Button.largeur_actuelle) - width_scale(400, Button.largeur_actuelle))
        # Lorsque l'on clique sur le bouton yes_raise
        case "yes_raise":
            if round(((Global_objects.connected_account[2]/100)*Global_objects.raised_amount)*100) > 0:
                send_action(Global_objects.client_socket,("bet",round(((Global_objects.connected_account[2]/100)*Global_objects.raised_amount)*100))) # INSERER MONTANT DU RAISE AVANT LAPPEL
            else:
                send_action(Global_objects.client_socket,("bet",0))
            Global_objects.is_raising = False
            Global_objects.buttons_interactibles = True
            Global_objects.game_state.timer[0] = 0
        # Lorsque l'on clique sur le bouton no_raise
        case "no_raise":
            Global_objects.is_raising = False
            Global_objects.buttons_interactibles = True