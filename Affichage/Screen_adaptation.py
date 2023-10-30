"""Document contenant les deux fonctions (une pour la largeur, l'autre pour la hauteur) permettant d'adapter tout ce qui s'affiche à l'écran par rapport à la taille de l'écran en question"""


def width_scale(largeur : int, largeur_screen : int, arrondi : bool = False) -> float | int:
    """Fonction qui permet de donner une largeur adaptée à la largeur de l'écran (par rapport à un écran de 17 pouces/1920px)

    Args:
        largeur (int): largeur à transformer
        largeur_screen (int): largeur de l'écran
        arrondi (bool): arrondir ou non le calcul (requis dans certains cas quand les virgules ne sont pas prises en compte)

    Returns:
        width (int): largeur adaptée
    """
    if arrondi:
        return round(largeur*largeur_screen/1921)
    else:
        return largeur*largeur_screen/1921

def height_scale(hauteur : int, hauteur_screen : int, arrondi : bool = False) -> float | int:
    """Fonction qui permet de donner une hauteur adaptée à la hauteur de l'écran (par rapport à un écran de 17 pouces/1080px)

    Args:
        hauteur (int): hauteur à transformer
        hauteur_screen (int): hauteur de l'écran
        arrondi (bool): arrondir ou non le calcul (requis dans certains cas quand les virgules ne sont pas prises en compte)

    Returns:
        height (int): hauteur adaptée
    """
    if arrondi:
        return round(hauteur*hauteur_screen/1081)
    else:
        return hauteur*hauteur_screen/1081