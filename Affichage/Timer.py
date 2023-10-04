# fonction timer


from time import time


def timer(durée : float, temps_depart : float):
    return durée - (time() - temps_depart)