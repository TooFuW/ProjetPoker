#Menu du jeu Poker

import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Chargez l'image de fond
fond = pygame.image.load("C:/Users/Utilisateur/ProjetPoker/PokerBackground.jpg")
fond = pygame.transform.scale(fond, (1280, 720))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dessinez l'image de fond sur la surface de l'écran
    screen.blit(fond, (0, 0))

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()


















#fonction importante pour plus tard à laisser en bas 
def str_to_list(string: str):   #fonctionne seulement sur une liste supposée valide
    liste = []
    string = string.removeprefix("[")
    string = string.removesuffix("]")

    return string.split(",")