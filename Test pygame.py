import pygame

class ScrollBox:
    def __init__(self, x, y, width, height, servers):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.servers = servers
        self.scroll_pos = 0

    def draw(self, surface):
        # Dessin de la boîte
        pygame.draw.rect(surface, "#D74B4B", (self.x, self.y, self.width, self.height))

        # Calcul de la zone d'affichage des éléments
        display_area = pygame.Rect(self.x, self.y, self.width, self.height)

        # Décalage vertical initial
        item_offset_y = 0

        # Dessin des éléments visibles
        indentation = "                    "
        for i, server in enumerate(self.servers[self.scroll_pos:]):
            item_y = self.y + item_offset_y
            item_rect = pygame.Rect(self.x, item_y, self.width, 40)
            if item_rect.colliderect(display_area):
                pygame.draw.rect(surface, "#475F77", item_rect)
                font = pygame.font.Font(None, 24)
                infos = server[0] + indentation + "Size of the table : " + str(server[1])
                text = font.render(infos, True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.topleft = (self.x + 5, item_y + 2)
                surface.blit(text, text_rect)

            # Ajouter un padding vertical entre chaque serveur
            item_offset_y += 40 + 5  # Ajouter 5 pixels de padding vertical

    def scroll_up(self):
        if self.scroll_pos > 0:
            self.scroll_pos -= 1

    def scroll_down(self):
        if self.scroll_pos < len(self.servers) - (self.height // 40):
            self.scroll_pos += 1

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


server_list = [["Lobby 1", 15], ["Lobby 2", 10], ["Lobby 3", 20], ["Lobby 4", 5], ["Lobby 5", 8], ["Lobby 6", 8], ["Lobby 7", 11], ["Lobby 8", 18], ["Lobby 9", 12], ["Lobby 10", 3]]
scrollbox = ScrollBox(100, 100, 800, 300, server_list)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Molette de la souris vers le haut
                scrollbox.scroll_up()
            elif event.button == 5:  # Molette de la souris vers le bas
                scrollbox.scroll_down()

    screen.fill("purple")

    # Dessinez la scrollbox
    scrollbox.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)
