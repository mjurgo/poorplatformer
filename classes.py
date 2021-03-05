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
        self.hitbox = pygame.Rect(self.rect.x + 12, self.rect.y, self.rect.width-25,
                            self.rect.height)
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
        self.alive = True

    def update(self, surface, map):
        self.move(map)
        
        # Handle sprite animation
        animation_cooldown = 100
        self.image = self.sprites[self.action][self.action_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.action_index += 1
        if self.action_index >= len(self.sprites[self.action]):
            self.action_index = 0

        # Draw player to the surface
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return self.alive

    def move(self, map):
        # Handle player movement
        dx = 0
        dy = 0
        scrollx = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and not self.jumping and not self.in_air:
            self.vel_y = -10
            self.jumping = True
        if not key[pygame.K_UP]:
            self.jumping = False
        if key[pygame.K_RIGHT]:
            if self.rect.x >= 380:
                scrollx -= 2
            else:
                dx += 2
            self.action = 2
        if key[pygame.K_LEFT]:
            if self.rect.x <= 100:
                scrollx += 2
            else:
                dx -= 2
            self.action = 1
        if not key[pygame.K_RIGHT] and not key[pygame.K_LEFT]:
            self.action = 0
            if self.action_index >= len(self.sprites[self.action]):
                self.action_index = 0

        # Handle gravity
        self.vel_y += 1
        if self.vel_y > 5:
            self.vel_y = 5
        dy += self.vel_y

        # Check for collisions with map elements
        self.in_air = True
        for tile in map.tile_group:
            if tile.solid:
                # Check for collisions in x direction
                if (tile.rect.colliderect(self.hitbox.x + dx, self.hitbox.y,
                        self.hitbox.width, self.hitbox.height) or
                        tile.rect.colliderect(self.hitbox.x - scrollx, self.hitbox.y,
                            self.hitbox.width, self.hitbox.height)):
                    dx = 0
                    scrollx = 0
                # Check for collisions in y direction
                if tile.rect.colliderect(self.hitbox.x, self.hitbox.y + dy,
                        self.hitbox.width, self.hitbox.height):
                    if self.vel_y < 0:
                        dy = tile.rect.bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile.rect.top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
        
        # Check for collisions with enemies
            for enemy in map.enemy_group:
                    if self.hitbox.colliderect(enemy.hitbox) and enemy.alive:
                        self.alive = False

        self.rect.x += dx
        self.rect.y += dy
        self.hitbox.x = self.rect.x + 12
        self.hitbox.y = self.rect.y
        self.hitbox.width = self.rect.width - 25
        self.hitbox.height = self.rect.height
        map.scroll(scrollx)


class Goblin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.idle = []
        self.run_right = []
        self.run_left = []
        # Load idle images
        for i in range(4):
            img = pygame.image.load(f'assets/goblin/idle{i}.png')
            self.idle.append(img)
        # Load run images
        for i in range(6):
            img = pygame.image.load(f'assets/goblin/run{i}.png')
            img_left = pygame.transform.flip(img, True, False)
            self.run_right.append(img)
            self.run_left.append(img_left)
        self.action = 0 # 0: idle, 1: walk left, 2: walk right
        self.sprites = {
            0: self.idle,
            1: self.run_left,
            2: self.run_right
        }
        self.alive = True
        self.image = self.sprites[0][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.action_index = 0
        self.update_time = pygame.time.get_ticks()
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y + 2,
                                self.rect.width - 3, self.rect.height - 2)

    def update(self, player, map, surface):
        # Handle sprite animation
        animation_cooldown = 100
        self.image = self.sprites[self.action][self.action_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.action_index += 1
        if self.action_index >= len(self.sprites[self.action]):
            self.action_index = 0

        # Detect player
        player_distance = self.rect.x - player.rect.x
        move_speed = 0
        if (player_distance > 0 and player_distance <= 100 and
                self.next_step_safe(map, 1)):
            self.action = 1
            self.rect.x -= 1
        elif (player_distance >= -100 and player_distance < 0 and
                self.next_step_safe(map, 2)):
            self.action = 2
            self.rect.x += 1
        else:
            self.action = 0
            if self.action_index >= len(self.sprites[self.action]):
                self.action_index = 0

        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y + 2
        pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 1)

    def next_step_safe(self, map, dir):
        for tile in map.tile_group:
            if dir == 1:
                if pygame.rect.Rect(self.rect.left - self.rect.width,
                                    self.rect.top, self.rect.width,
                                    self.rect.height + 1).colliderect(tile.rect):
                    return True
            elif dir == 2:
                if pygame.rect.Rect(self.rect.right,
                                    self.rect.top, self.rect.width,
                                    self.rect.height + 1).colliderect(tile.rect):
                    return True
        return False


class Map:
    def __init__(self):
        img = pygame.image.load('assets/background.png')
        self.background = pygame.transform.scale(img, (1280, 720))
        self.tiled_map = pytmx.load_pygame('assets/maps/testmap2.tmx')
        self.tile_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        # Load ground tiles
        for x, y, gid in self.tiled_map.get_layer_by_name('Ground'):
            tile_img = self.tiled_map.get_tile_image_by_gid(gid)
            if tile_img:
                solid = self.tiled_map.get_tile_properties_by_gid(gid).get('solid') or False
                tile = Tile(tile_img, x * self.tiled_map.tilewidth,
                    (y * self.tiled_map.tileheight) +
                    (self.tiled_map.tileheight - tile_img.get_height()),
                    solid=solid)
                self.tile_group.add(tile)

        # Load enemies
        for enemy in self.tiled_map.get_layer_by_name('Enemies'):
            if enemy.properties.get('goblin'):
                goblin = Goblin(enemy.x, enemy.y)
                self.enemy_group.add(goblin)

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

    def scroll(self, scrollx):
        for tile in self.tile_group:
            tile.rect.x += scrollx
        for enemy in self.enemy_group:
            enemy.rect.x += scrollx


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
