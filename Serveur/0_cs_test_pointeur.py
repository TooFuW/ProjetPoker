from random import randint
from time import sleep
from threading import *


fonctions_id_dict = {}

def get_info():
    id_fonctions_id_dict = 457
    fonctions_id_dict[id_fonctions_id_dict] = None

    res = fonctions_id_dict[id_fonctions_id_dict]
    cpt = 0

    thread_info_sender = Thread(target=info_sender, args=[id_fonctions_id_dict])
    thread_info_sender.start()

    while res is None and cpt < 30:
        print(cpt)
        res = fonctions_id_dict[id_fonctions_id_dict]
        sleep(0.35)
        cpt += 1

    del fonctions_id_dict[id_fonctions_id_dict]
    return res

def info_sender(id_fonctions_id_dict):

    cpt = 5
    for _ in range(5):
        print("envoi dans ",cpt)
        cpt -= 1
        sleep(1)

    fonctions_id_dict[id_fonctions_id_dict] = True
    


print(get_info())