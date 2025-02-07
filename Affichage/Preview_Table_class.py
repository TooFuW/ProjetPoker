"""Document contenant la classe Preview_Table qui permet d'afficher une preview d'un serveur sélectionné"""


import pygame
from Screen_adaptation import *
from Button_class import *


class Preview_Table:
    """Classe Preview_Table pour afficher des previews de tables
    """

    def __init__(self, largeur_actuelle : int, hauteur_actuelle : int, screen : pygame.Surface, fond : pygame.Surface, pos : tuple, join_button : bool = True):
        """Initialisation des paramètres des previews

        Args:
            largeur_actuelle (int): Largeur de l'écran (pour width_scale())
            hauteur_actuelle (int): Hauteur de l'écran (pour height_scale())
            screen (pygame.Surface): Ecran sur lequel afficher la fenêtre (écran de l'utilisateur)
            fond (pygame.Surface): Surface du fond du widget
            pos (tuple): Position x, y de la preview (x : largeur, y : hauteur)
            join_button (bool) = True: Si on doit ou non mettre un bouton join
        """
        self.largeur_actuelle = largeur_actuelle
        self.hauteur_actuelle = hauteur_actuelle
        self.screen = screen
        self.fond = fond
        self.x = width_scale(pos[0], largeur_actuelle)
        self.y = height_scale(pos[1], hauteur_actuelle)
        self.width = width_scale(600, largeur_actuelle)
        if join_button:
            self.height = height_scale(600, hauteur_actuelle)
            # Création de l'objet jointablebutton
            self.jointablebutton = Button(self.largeur_actuelle, self.hauteur_actuelle, self.screen, "join table", "JOIN", "Roboto", 50, (255, 255, 255), (0, 0, 0, 180), (50, 50, 50, 200), (90, 90, 90, 180), (0, 0, 0), 3, 600 - 440, 600 - 530, (pos[0] + 220, pos[1] + 520), 10)
        else:
            self.height = height_scale(510, hauteur_actuelle)
            self.jointablebutton = False
        # Une liste contenant tous les joueurs dans la table sélectionnée sous la forme [sit_id, idplayer, pseudo, chips, link] par joueur
        self.players = []

    def draw(self):
        """Génération/affichage de la preview
        """
        # Dessinez la zone de la preview sur l'écran
        pygame.draw.rect(self.screen, "#006400", (self.x, self.y, self.width, self.height), border_radius = 10)
        # Dessine l'image de fond sur la self.screen de l'écran
        fond = pygame.transform.scale(self.fond, (width_scale(580, self.largeur_actuelle), height_scale(490, self.hauteur_actuelle)))
        self.screen.blit(fond, (self.x + width_scale( 10, self.largeur_actuelle), self.y + height_scale( 10, self.hauteur_actuelle)))
        if self.jointablebutton is not False:
            # Affichage des bouttons
            # Cliquer sur le bouton JOIN fait rejoindre la table sélectionnée
            self.jointablebutton.draw()
        # Pour chaque joueur dans la table on affiche ses informations
        gui_font = pygame.font.SysFont("Roboto", width_scale(30, self.largeur_actuelle, True))
        match len(self.players):

            case 2:
                # On affiche les boxs
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(225, self.largeur_actuelle), self.y + height_scale(165, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(225, self.largeur_actuelle), self.y + height_scale(265, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                # On affiche les textes au-dessus des boxs correspondants
                # Texte box 1
                if self.players[0][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[0][1]}\n{self.players[0][2]}"
                    text = text.replace("'", "")
                height = 170
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(230, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 2
                if self.players[1][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[1][1]}\n{self.players[1][2]}"
                    text = text.replace("'", "")
                height = 270
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(230, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25

            case 3:
                # On affiche les boxs
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(225, self.largeur_actuelle), self.y + height_scale(115, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(225, self.largeur_actuelle), self.y + height_scale(215, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(225, self.largeur_actuelle), self.y + height_scale(315, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                # On affiche les textes au-dessus des boxs correspondants
                # Texte box 1
                if self.players[0][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[0][1]}\n{self.players[0][2]}"
                    text = text.replace("'", "")
                height = 120
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(230, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 2
                if self.players[1][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[1][1]}\n{self.players[1][2]}"
                    text = text.replace("'", "")
                height = 220
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(230, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 3
                if self.players[2][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[2][1]}\n{self.players[2][2]}"
                    text = text.replace("'", "")
                height = 320
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(230, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25

            case 4:
                # On affiche les boxs
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(225, self.largeur_actuelle), self.y + height_scale(70, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(225, self.largeur_actuelle), self.y + height_scale(170, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(225, self.largeur_actuelle), self.y + height_scale(270, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(225, self.largeur_actuelle), self.y + height_scale(370, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                # On affiche les textes au-dessus des boxs correspondants
                # Texte box 1
                if self.players[0][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[0][1]}\n{self.players[0][2]}"
                    text = text.replace("'", "")
                height = 75
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(230, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 2
                if self.players[1][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[1][1]}\n{self.players[1][2]}"
                    text = text.replace("'", "")
                height = 175
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(230, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 3
                if self.players[2][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[2][1]}\n{self.players[2][2]}"
                    text = text.replace("'", "")
                height = 275
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(230, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 4
                if self.players[3][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[3][1]}\n{self.players[3][2]}"
                    text = text.replace("'", "")
                height = 375
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(230, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25

            case 5:
                # On affiche les boxs
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(225, self.largeur_actuelle), self.y + height_scale(65, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(165, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(165, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(265, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(265, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                # On affiche les textes au-dessus des boxs correspondants
                # Texte box 1
                if self.players[0][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[0][1]}\n{self.players[0][2]}"
                    text = text.replace("'", "")
                height = 70
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(230, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 2
                if self.players[1][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[1][1]}\n{self.players[1][2]}"
                    text = text.replace("'", "")
                height = 170
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 3
                if self.players[2][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[2][1]}\n{self.players[2][2]}"
                    text = text.replace("'", "")
                height = 170
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 4
                if self.players[3][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[3][1]}\n{self.players[3][2]}"
                    text = text.replace("'", "")
                height = 270
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 5
                if self.players[4][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[4][1]}\n{self.players[4][2]}"
                    text = text.replace("'", "")
                height = 270
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25

            case 6:
                # On affiche les boxs
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(225, self.largeur_actuelle), self.y + height_scale(65, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(165, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(165, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(265, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(265, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(225, self.largeur_actuelle), self.y + height_scale(365, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                # On affiche les textes au-dessus des boxs correspondants
                # Texte box 1
                if self.players[0][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[0][1]}\n{self.players[0][2]}"
                    text = text.replace("'", "")
                height = 70
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(230, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 2
                if self.players[1][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[1][1]}\n{self.players[1][2]}"
                    text = text.replace("'", "")
                height = 170
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 3
                if self.players[2][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[2][1]}\n{self.players[2][2]}"
                    text = text.replace("'", "")
                height = 170
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 4
                if self.players[3][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[3][1]}\n{self.players[3][2]}"
                    text = text.replace("'", "")
                height = 270
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 5
                if self.players[4][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[4][1]}\n{self.players[4][2]}"
                    text = text.replace("'", "")
                height = 270
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 6
                if self.players[5][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[5][1]}\n{self.players[5][2]}"
                    text = text.replace("'", "")
                height = 370
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(230, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25

            case 7:
                # On affiche les boxs
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(65, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(65, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(165, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(165, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(265, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(265, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(225, self.largeur_actuelle), self.y + height_scale(365, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                # On affiche les textes au-dessus des boxs correspondants
                # Texte box 1
                if self.players[0][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[0][1]}\n{self.players[0][2]}"
                    text = text.replace("'", "")
                height = 70
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 2
                if self.players[1][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[1][1]}\n{self.players[1][2]}"
                    text = text.replace("'", "")
                height = 70
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 3
                if self.players[2][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[2][1]}\n{self.players[2][2]}"
                    text = text.replace("'", "")
                height = 170
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 4
                if self.players[3][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[3][1]}\n{self.players[3][2]}"
                    text = text.replace("'", "")
                height = 170
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 5
                if self.players[3][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[4][1]}\n{self.players[4][2]}"
                    text = text.replace("'", "")
                height = 270
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 6
                if self.players[5][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[5][1]}\n{self.players[5][2]}"
                    text = text.replace("'", "")
                height = 270
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 7
                if self.players[6][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[6][1]}\n{self.players[6][2]}"
                    text = text.replace("'", "")
                height = 370
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(230, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25

            case 8:
                # On affiche les boxs
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(65, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(65, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(165, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(165, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(265, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(265, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(365, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(365, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                # On affiche les textes au-dessus des boxs correspondants
                # Texte box 1
                if self.players[0][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[0][1]}\n{self.players[0][2]}"
                    text = text.replace("'", "")
                height = 70
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 2
                if self.players[1][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[1][1]}\n{self.players[1][2]}"
                    text = text.replace("'", "")
                height = 70
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 3
                if self.players[2][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[2][1]}\n{self.players[2][2]}"
                    text = text.replace("'", "")
                height = 170
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 4
                if self.players[3][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[3][1]}\n{self.players[3][2]}"
                    text = text.replace("'", "")
                height = 170
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 5
                if self.players[4][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[4][1]}\n{self.players[4][2]}"
                    text = text.replace("'", "")
                height = 270
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 6
                if self.players[5][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[5][1]}\n{self.players[5][2]}"
                    text = text.replace("'", "")
                height = 270
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 7
                if self.players[6][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[6][1]}\n{self.players[6][2]}"
                    text = text.replace("'", "")
                height = 370
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 8
                if self.players[7][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[7][1]}\n{self.players[7][2]}"
                    text = text.replace("'", "")
                height = 370
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25

            case 9:
                # On affiche les boxs
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(65, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(225, self.largeur_actuelle), self.y + height_scale(65, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(65, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(165, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(165, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(265, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(265, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(365, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(365, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                # On affiche les textes au-dessus des boxs correspondants
                # Texte box 1
                if self.players[0][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[0][1]}\n{self.players[0][2]}"
                    text = text.replace("'", "")
                height = 70
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 2
                if self.players[1][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[1][1]}\n{self.players[1][2]}"
                    text = text.replace("'", "")
                height = 70
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(230, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 3
                if self.players[2][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[2][1]}\n{self.players[2][2]}"
                    text = text.replace("'", "")
                height = 70
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 4
                if self.players[3][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[3][1]}\n{self.players[3][2]}"
                    text = text.replace("'", "")
                height = 170
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 5
                if self.players[4][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[4][1]}\n{self.players[4][2]}"
                    text = text.replace("'", "")
                height = 170
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 6
                if self.players[5][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[5][1]}\n{self.players[5][2]}"
                    text = text.replace("'", "")
                height = 270
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 7
                if self.players[6][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[6][1]}\n{self.players[6][2]}"
                    text = text.replace("'", "")
                height = 270
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 8
                if self.players[7][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[7][1]}\n{self.players[7][2]}"
                    text = text.replace("'", "")
                height = 370
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 9
                if self.players[8][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[8][1]}\n{self.players[8][2]}"
                    text = text.replace("'", "")
                height = 370
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25

            case 10:
                # On affiche les boxs
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(65, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(225, self.largeur_actuelle), self.y + height_scale(65, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(65, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(165, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(165, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(265, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(265, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), self.y + height_scale(365, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(225, self.largeur_actuelle), self.y + height_scale(365, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(400, self.largeur_actuelle), self.y + height_scale(365, self.hauteur_actuelle)), (width_scale(600 - 450, self.largeur_actuelle), height_scale(600 - 530, self.hauteur_actuelle))), border_radius = 3)
                # On affiche les textes au-dessus des boxs correspondants
                # Texte box 1
                if self.players[0][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[0][1]}\n{self.players[0][2]}"
                    text = text.replace("'", "")
                height = 70
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 2
                if self.players[1][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[1][1]}\n{self.players[1][2]}"
                    text = text.replace("'", "")
                height = 70
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(230, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 3
                if self.players[2][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[2][1]}\n{self.players[2][2]}"
                    text = text.replace("'", "")
                height = 70
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 4
                if self.players[3][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[3][1]}\n{self.players[3][2]}"
                    text = text.replace("'", "")
                height = 170
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 5
                if self.players[4][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[4][1]}\n{self.players[4][2]}"
                    text = text.replace("'", "")
                height = 170
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 6
                if self.players[5][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[5][1]}\n{self.players[5][2]}"
                    text = text.replace("'", "")
                height = 270
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 7
                if self.players[6][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[6][1]}\n{self.players[6][2]}"
                    text = text.replace("'", "")
                height = 270
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 8
                if self.players[7][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[7][1]}\n{self.players[7][2]}"
                    text = text.replace("'", "")
                height = 370
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 9
                if self.players[8][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[8][1]}\n{self.players[8][2]}"
                    text = text.replace("'", "")
                height = 370
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(230, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25
                # Texte box 10
                if self.players[9][1] == None:
                    text = "Sit Available"
                else:
                    text = f"{self.players[9][1]}\n{self.players[9][2]}"
                    text = text.replace("'", "")
                height = 370
                for elem in text.split("\n"):
                    text_surf = gui_font.render(elem, True, "#FFFFFF")
                    self.screen.blit(text_surf, (self.x + width_scale(405, self.largeur_actuelle), self.y + height_scale(height, self.hauteur_actuelle)))
                    height += 25