import pygame

from classes import Map


pygame.init()

# Screen configuration
width, height = (1280, 720)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Poor platformer')

game_surface = pygame.Surface((480, 272))

# Set FPS
clock = pygame.time.Clock()
fps = 60

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
    screen.blit(pygame.transform.scale(game_surface, (width, height)), (0, 0))

    pygame.display.update()

pygame.quit()
