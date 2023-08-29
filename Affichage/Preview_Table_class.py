# Preview_Table class


import pygame
from Screen_adaptation import *
import Button_class


class Preview_Table:
    """Classe Preview_Table pour afficher des previews de tables
    """

    def __init__(self, largeur_actuelle : int, hauteur_actuelle : int, screen : pygame.Surface, poker_table : pygame.Surface, pos : tuple, scale : float = 1):
        """Initialisation des paramètres des previews

        Args:
            largeur_actuelle (int): Largeur de l'écran (pour width_scale())
            hauteur_actuelle (int): Hauteur de l'écran (pour height_scale())
            screen (pygame.Surface): Ecran sur lequel afficher la fenêtre (écran de l'utilisateur)
            poker_table (pygame.Surface): Table de poker pour fond du widget
            pos (tuple): Position x, y de la preview
            scale (float) = 1: Multiplicateur de taille de la preview (1 par défaut)
        """
        self.largeur_actuelle = largeur_actuelle
        self.hauteur_actuelle = hauteur_actuelle
        self.screen = screen
        self.poker_table = poker_table
        self.x = width_scale(pos[0], largeur_actuelle)
        self.y = height_scale(pos[1], hauteur_actuelle)
        self.width = width_scale(600*scale, largeur_actuelle)
        self.height = height_scale(600*scale, hauteur_actuelle)
        self.scale = scale
        # Une liste contenant tous les joueurs dans la table sélectionnée
        self.players = [["sit_id", "idplayer", "pseudo", "chips", "link"], ["sit_id", "idplayer", "pseudo", "chips", "link"], ["sit_id", "idplayer", "pseudo", "chips", "link"], ["sit_id", "idplayer", "pseudo", "chips", "link"], ["sit_id", "idplayer", "pseudo", "chips", "link"], ["sit_id", "idplayer", "pseudo", "chips", "link"]]
        # Création de l'objet jointablebutton
        self.jointablebutton = Button_class.Button(self.largeur_actuelle, self.hauteur_actuelle, self.screen, "join table", "JOIN", "Roboto", 50, "#475F77", "#354B5E", "#D74B4B", "#354B5E", 600*scale - 440, 600*scale - 530, (pos[0] + 220, pos[1] + 520), 6, 10)

    def draw(self):
        """Génération/affichage de la preview
        """
        # Dessinez la zone de la preview sur l'écran
        pygame.draw.rect(self.screen, "#006400", (self.x, self.y, self.width, self.height), border_radius = 10)
        # Dessine l'image de fond sur la self.screen de l'écran
        poker_table = pygame.transform.scale(self.poker_table, (width_scale(580*self.scale, self.largeur_actuelle), height_scale(490*self.scale, self.hauteur_actuelle)))
        self.screen.blit(poker_table, (self.x + width_scale( 10, self.largeur_actuelle), self.y + height_scale( 10, self.hauteur_actuelle)))
        # Affichage des bouttons
        # Cliquer sur le bouton JOIN fait rejoindre la table sélectionnée
        self.jointablebutton.draw()
        # Pour chaque joueur dans la table on affiche ses informations
        temp_x = self.x
        temp_y = self.y
        player_count = 0
        for player in self.players:
            player_count += 1
            if player_count >= 5:
                pass
            # On génére le texte
            gui_font = pygame.font.SysFont("Roboto", width_scale(30, self.largeur_actuelle))
            text_info = f"{player[2]}\n{player[3]}"
            # On affiche la box derrière le texte
            pygame.draw.rect(self.screen, "#475F77", pygame.Rect((self.x + width_scale(50, self.largeur_actuelle), temp_y + height_scale(55, self.hauteur_actuelle)), (width_scale(600*self.scale - 450, self.largeur_actuelle), height_scale(600*self.scale - 530, self.hauteur_actuelle))), border_radius = 3)
            # On affiche le texte en sautant une ligne pour chaque info différente du joueur
            y = 60
            for ligne in text_info.split("\n"):
                text_surf = gui_font.render(ligne, True, "#FFFFFF")
                self.screen.blit(text_surf, (self.x + width_scale(55, self.largeur_actuelle), temp_y + height_scale(y, self.hauteur_actuelle)))
                y += 25
            temp_y += height_scale(80, self.hauteur_actuelle)