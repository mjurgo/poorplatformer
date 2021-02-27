import pygame

# Define function for drawing text
def draw_text(surface, text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    surface.blit(img, (x, y))
