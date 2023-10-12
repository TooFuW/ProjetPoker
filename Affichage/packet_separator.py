"""Document contenant la fonction packet_separator pour récupérer les infos voulues d'un packet donné"""

def packet_separator(chaine):
    """Permet de séparer les infos dans un paquet donné"""
    gauche=""
    droite=""
    premieregal=False
    for i in chaine:
        if not premieregal:
            if i != "=":
                gauche+=i
            else:
                premieregal=True
        else:
            droite+=i
    return (gauche,droite)