import pygame
import sys

from level import Level
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Platformer')
clock = pygame.time.Clock()

level = Level()

while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG_COLOR)
    level.run()

    # Drawing logic
    pygame.display.update()
    clock.tick(60)
