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
        self.action = 0 # 0: idle, 1: run left, 2: run right
        self.sprites = {
            0: self.idle_right,
            1: self.run_left,
            2: self.run_right
        }
        self.vel_y = 0
        self.jumping = False
        self.in_air = True

    def update(self, map):
        # Handle sprite animation
        animation_cooldown = 100
        self.image = self.sprites[self.action][self.action_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.action_index += 1
        if self.action_index >= len(self.idle_right):
            self.action_index = 0

        self.move(map)


    def move(self, map):
        # Handle player movement
        dx = 0
        dy = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and not self.jumping and not self.in_air:
            self.vel_y = -10
            self.jumping = True
        if not key[pygame.K_UP]:
            self.jumping = False
        if key[pygame.K_RIGHT]:
            dx += 2
            self.action = 2
        if key[pygame.K_LEFT]:
            dx -= 2
            self.action = 1
        if not key[pygame.K_RIGHT] and not key[pygame.K_LEFT]:
            self.action = 0

        # Handle gravity
        self.vel_y += 1
        if self.vel_y > 5:
            self.vel_y = 5
        dy += self.vel_y

        # Check for collisions with map elements
        self.in_air = True
        for tile in map.tile_group:
            # Check for collisions in x direction
            # if pygame.sprite.spritecollide(self, map.tile_group, False):
            #     print('collision')
            if tile.solid:
                if tile.rect.colliderect(self.rect.x + dx, self.rect.y,
                        self.rect.width, self.rect.height):
                    dx = 0
                # Check for collisions in y direction
                if tile.rect.colliderect(self.rect.x, self.rect.y + dy,
                        self.rect.width, self.rect.height):
                    if self.vel_y < 0:
                        dy = tile.rect.bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile.rect.top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False


        self.rect.x += dx
        self.rect.y += dy


class Map:
    def __init__(self):
        img = pygame.image.load('assets/background.png')
        self.background = pygame.transform.scale(img, (1280, 720))
        self.tiled_map = pytmx.load_pygame('assets/maps/testmap2.tmx')
        self.tile_group = pygame.sprite.Group()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        for layer in self.tiled_map.visible_layers:
            for x, y, gid in layer:
                tile_img = self.tiled_map.get_tile_image_by_gid(gid)
                if tile_img:
                    solid = self.tiled_map.get_tile_properties_by_gid(gid).get('solid') or False
                    tile = Tile(tile_img, x * self.tiled_map.tilewidth,
                        y * self.tiled_map.tileheight, solid=solid)
                    self.tile_group.add(tile)


class Tile(pygame.sprite.Sprite):
    def __init__(self, img, x, y, solid=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.solid = solid

    # def update(self, surface):
    #     pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)
