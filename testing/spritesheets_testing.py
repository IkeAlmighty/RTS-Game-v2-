import pygame, sys
sys.path.append(".")
import spritesheets
from spritesheets import *

spritesheet = SpriteSheet("../assets/tree_1.png")

pygame.init()

screen = pygame.display.set_mode((800, 600))

running = True

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type is pygame.KEYDOWN and event.key is pygame.K_ESCAPE:
            running = False

    screen.fill((255, 255, 255))
    screen.blit(spritesheet.next(), (0, 0))

    pygame.display.flip()

    clock.tick(2)