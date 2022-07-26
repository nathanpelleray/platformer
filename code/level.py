import pygame
from pytmx.util_pygame import load_pygame

from settings import LEVEL_MAP, TILE_SIZE, CAMERA_BORDERS
from tile import Tile
from player import Player


class Level:
    def __init__(self):
        # Level setup
        self.player = None
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup
        self.visible_sprites = CameraGroup()
        self.active_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup_level()

    def setup_level(self):
        tmx_data = load_pygame('../map/tmx/map_test.tmx', pixelalpha=True)

        # Map
        for layout in tmx_data.visible_layers:
            if hasattr(layout, 'data'):
                for x, y, surf in layout.tiles():
                    x *= TILE_SIZE
                    y *= TILE_SIZE
                    Tile((x, y), surf, [self.visible_sprites, self.collision_sprites])

        # Entities
        for obj in tmx_data.objects:
            x = obj.x
            y = obj.y
            if obj.type == 'player':
                self.player = Player((x, y), [self.visible_sprites, self.active_sprites], self.collision_sprites)

    def run(self):
        # Run the entire game (level)
        self.active_sprites.update()
        self.visible_sprites.custom_draw(self.player)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(100, 300)

        # Center camera setup
        # self.half_w = self.display_surface.get_size()[0] // 2
        # self.half_h = self.display_surface.get_size()[1] // 2

        # Camera
        cam_left = CAMERA_BORDERS['left']
        cam_top = CAMERA_BORDERS['top']
        cam_width = self.display_surface.get_size()[0] - (cam_left + CAMERA_BORDERS['right'])
        cam_height = self.display_surface.get_size()[1] - (cam_top + CAMERA_BORDERS['bottom'])

        self.camera_rect = pygame.Rect(cam_left, cam_top, cam_width, cam_height)

    def custom_draw(self, player):
        # Get the player offset
        # self.offset.x = player.rect.centerx - self.half_w
        # self.offset.y = player.rect.centery - self.half_h

        # Getting the camera position
        if player.rect.left < self.camera_rect.left:
            self.camera_rect.left = player.rect.left
        if player.rect.right > self.camera_rect.right:
            self.camera_rect.right = player.rect.right
        if player.rect.top < self.camera_rect.top:
            self.camera_rect.top = player.rect.top
        if player.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = player.rect.bottom

        # Camera offset
        self.offset = pygame.math.Vector2(self.camera_rect.left - CAMERA_BORDERS['left'],
                                          self.camera_rect.top - CAMERA_BORDERS['top'])

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
