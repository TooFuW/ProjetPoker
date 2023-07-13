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
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)

        # Calcul de la zone d'affichage des éléments
        display_area = pygame.Rect(self.x, self.y, self.width, self.height)

        # Dessin des éléments visibles
        for i, server in enumerate(self.servers[self.scroll_pos:]):
            item_y = self.y + (i * 20)
            item_rect = pygame.Rect(self.x, item_y, self.width, 20)
            if item_rect.colliderect(display_area):
                pygame.draw.rect(surface, (200, 200, 200), item_rect)
                font = pygame.font.Font(None, 18)
                text = font.render(server, True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.topleft = (self.x + 5, item_y + 2)
                surface.blit(text, text_rect)
    
    def scroll_up(self):
        if self.scroll_pos > 0:
            self.scroll_pos -= 1

    def scroll_down(self):
        if self.scroll_pos < len(self.servers) - (self.height // 20):
            self.scroll_pos += 1

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


server_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
scrollbox = ScrollBox(100, 100, 200, 300, server_list)

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

    pygame.display.flip()
    clock.tick(60)
