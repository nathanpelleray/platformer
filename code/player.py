import pygame

from utils import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)

        # Player movement
        self.wall_jump_time = None
        self.on_jump = False
        self.jump_cooldown = 200
        self.direction = pygame.math.Vector2()
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = 16
        self.collision_sprites = collision_sprites
        self.on_floor = False

        # Animation
        self.animations = None
        self.frame_index = 0
        self.animation_speed = 0.15
        self.import_character_assets()
        self.image = self.animations['idle'][self.frame_index]

        # Dust particules
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = pygame.display.get_surface()

        # Player Status
        self.status = 'idle'
        self.facing_right = True
        self.slide_wall = False

        # Rect
        self.rect = self.image.get_rect(topleft=pos)

    def import_character_assets(self):
        character_path = '../graphics/player/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'slide_wall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]
        if self.slide_wall:
            animation = self.animations['slide_wall']

        # Loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.on_jump:
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.facing_right = True
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.facing_right = False
            else:
                self.direction.x = 0

            if keys[pygame.K_SPACE] and (self.on_floor or self.slide_wall):
                if self.slide_wall:
                    self.on_jump = True
                    self.wall_jump_time = pygame.time.get_ticks()

                    if self.facing_right:
                        self.direction.x = -1
                        self.facing_right = False
                    else:
                        self.direction.x = 1
                        self.facing_right = True
                self.direction.y = -self.jump_speed
                self.on_floor = False
                self.slide_wall = False

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.on_jump:
            if current_time - self.wall_jump_time >= self.jump_cooldown:
                self.on_jump = False

    def horizontal_collisions(self):
        # Simulate input for slide wall
        if self.slide_wall and self.facing_right:
            self.direction.x = 1
            self.rect.x += self.direction.x * self.speed
        elif self.slide_wall:
            self.direction.x = -1
            self.rect.x += self.direction.x * self.speed

        self.slide_wall = False
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.status == 'fall':
                    self.slide_wall = True
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left

    def vertical_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_floor = True

        if self.on_floor and self.direction.y != 0:
            self.on_floor = False

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

        if self.slide_wall:
            self.direction.y = 1.1
            self.rect.y += self.direction.y

    def update(self):
        self.input()
        self.cooldowns()
        self.rect.x += self.direction.x * self.speed
        self.horizontal_collisions()
        self.apply_gravity()
        self.vertical_collisions()
        self.get_status()
        self.animate()
