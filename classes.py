import pygame
import pytmx


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = None


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
