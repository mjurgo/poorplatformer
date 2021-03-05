import pygame

from classes import Map, Player
from functions import draw_text


pygame.init()

# Screen configuration
width, height = (1280, 720)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Poor platformer')

game_surface = pygame.Surface((480, 272))

# Set FPS
clock = pygame.time.Clock()
fps = 60

# Define colours
colour_yellow = (255, 255, 54)
colour_red = (255, 0, 0)

# Define fonts
font = pygame.font.SysFont('ubuntu', 15)
# font15 = pygame.font.SysFont('ubuntu', 15)
font20 = pygame.font.SysFont('ubuntu', 20)
font25 = pygame.font.SysFont('ubuntu', 25)

# Create game over surface
game_over = pygame.Surface((480, 272))
draw_text(game_over, 'GAME OVER', font25, colour_red, 168, 120)

# Create Player group
player = Player(20, 192)
player_group = pygame.sprite.GroupSingle()
player_group.add(player)

# Create current map
map = Map()

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
    map.draw(game_surface)
    map.tile_group.draw(game_surface)
    map.tile_group.update(game_surface)

    # Draw enemies
    map.enemy_group.draw(game_surface)
    map.enemy_group.update(player, map, game_surface)

    pygame.draw.rect(game_surface, (255, 0, 0), player.hitbox, 1)

    draw_text(game_surface, str(int(clock.get_fps())), font, colour_yellow, 10, 10)

    if player.update(game_surface, map):
        screen.blit(pygame.transform.scale(game_surface, (width, height)), (0, 0))
    else:
        screen.blit(pygame.transform.scale(game_over, (width, height)), (0, 0))
    # screen.blit(game_surface, (0, 0))

    pygame.display.update()

pygame.quit()
