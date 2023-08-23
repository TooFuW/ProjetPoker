def strtotuple(chaine):
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



            