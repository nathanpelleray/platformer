import pygame

from utils import import_folder
from settings import TILE_SIZE


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surf=pygame.Surface((TILE_SIZE, TILE_SIZE)), type=None):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.type = type


class AnimatedTile(Tile):
    def __init__(self, pos, path, groups, type):
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        super().__init__(pos, groups, self.image, type)

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()


class Coin(AnimatedTile):
    def __init__(self, pos, path, groups):
        super().__init__(pos, path, groups, 'coin')
