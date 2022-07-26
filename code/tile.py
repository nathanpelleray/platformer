import pygame

from settings import TILE_SIZE, TILE_COLOR


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        # self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image = surf
        # self.image.fill(TILE_COLOR)
        self.rect = self.image.get_rect(topleft=pos)
