# Objets Globaux

from time import *


Global_game_state = None
Global_accountbutton = None
Global_playbutton = None
Global_settingsbutton = None
Global_exitbutton = None
Global_backbutton = None
Global_createtablebutton = None
Global_gamehistorybutton = None
Global_deconnexionbutton = None
Global_accountsettingsbutton = None
Global_settingpage1button = None
Global_settingpage2button = None
Global_settingpage3button = None
Global_serverscrollbox = None
Global_historyscrollbox = None
Global_tablecodeinput = None
Global_accountpseudoinput = None
Global_accountinformationinput = None
Global_previewlobbys = None
Global_previewhistory = None

if Global_game_state != None:
        print(Global_game_state.back_pile)