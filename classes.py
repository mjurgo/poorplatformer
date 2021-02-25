import pygame
import pytmx


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.idle_right = []
        self.idle_left = []
        self.run_right = []
        self.run_left = []
        # load idle images
        for i in range(4):
            img = pygame.image.load(f'assets/player/idle{i}.png')
            img_left = pygame.transform.flip(img, True, False)
            self.idle_right.append(img)
            self.idle_left.append(img_left)
        # load run images
        for i in range(6):
            img = pygame.image.load(f'assets/player/run{i}.png')
            img_left = pygame.transform.flip(img, True, False)
            self.run_right.append(img)
            self.run_left.append(img_left)
        self.action_index = 0
        self.image = self.idle_right[self.action_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.update_time = pygame.time.get_ticks()

    def update(self):
        # Handle sprite animation
        animation_cooldown = 100
        self.image = self.idle_right[self.action_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.action_index += 1
        if self.action_index >= len(self.idle_right):
            self.action_index = 0


class Map:
    def __init__(self):
        img = pygame.image.load('assets/background.png')
        self.background = pygame.transform.scale(img, (1280, 720))
        self.tiled_map = pytmx.load_pygame('assets/maps/testmap2.tmx')

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        for layer in self.tiled_map.visible_layers:
            for x, y, gid in layer:
                tile = self.tiled_map.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * self.tiled_map.tilewidth,
                        y * self.tiled_map.tileheight))
