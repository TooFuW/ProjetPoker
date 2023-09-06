# Screen adaptation


def width_scale(largeur : int, largeur_screen : int) -> int:
    """Fonction qui permet de donner une largeur adaptée à la largeur de l'écran (par rapport à un écran de 17 pouces/1920px)

    Args:
        largeur (int): largeur à transformer
        largeur_screen (int): largeur de l'écran

    Returns:
        width (int): largeur adaptée
    """
    width = largeur*largeur_screen//1920
    return width

def height_scale(hauteur : int, hauteur_screen : int) -> int:
    """Fonction qui permet de donner une hauteur adaptée à la hauteur de l'écran (par rapport à un écran de 17 pouces/1080px)

    Args:
        hauteur (int): hauteur à transformer
        hauteur_screen (int): hauteur de l'écran

    Returns:
        height (int): hauteur adaptée
    """
    height = hauteur*hauteur_screen//1080
    return height