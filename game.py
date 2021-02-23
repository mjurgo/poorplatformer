import pygame


pygame.init()

# Screen configuration
width, height = (1280, 720)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Poor platformer')

# Set FPS
clock = pygame.time.Clock()
fps = 60

run = True
while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    pygame.display.update()

pygame.quit()
