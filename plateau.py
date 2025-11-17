import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 900, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plateau Monopoly - Pygame")

# Chargement du plateau
board_image = pygame.image.load("monopoly-classique-plateau.jpg")
board_image = pygame.transform.scale(board_image, (WIDTH, HEIGHT))

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(board_image, (0, 0))
    pygame.display.flip()

pygame.quit()
sys.exit()
