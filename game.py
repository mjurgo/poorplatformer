import pygame

from classes import Map, Player


pygame.init()

# Screen configuration
width, height = (1280, 720)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Poor platformer')

game_surface = pygame.Surface((480, 272))

# Set FPS
clock = pygame.time.Clock()
fps = 60

# Create Player group
player = Player(20, 192)
player_group = pygame.sprite.GroupSingle()
player_group.add(player)

run = True
while run:
    clock.tick(fps)

    # Listen for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    # Draw map
    map = Map()
    map.draw(game_surface)
    map.tile_group.draw(game_surface)
    map.tile_group.update(game_surface)

    # Draw player
    player_group.draw(game_surface)

    # Update player
    player_group.update(map)

    pygame.draw.rect(game_surface, (255, 0, 0), player.rect, 1)

    screen.blit(pygame.transform.scale(game_surface, (width, height)), (0, 0))
    # screen.blit(game_surface, (0, 0))

    pygame.display.update()

pygame.quit()
