import pygame
from pygame.locals import *
from topdowngameassets import *

screen_x,screen_y = 720,450
screen = pygame.display.set_mode((screen_x,screen_y))
pygame.display.set_caption("Top Down Test")
running = True
player = gameplayer()
tiles = wallcollider()
camera = gamecamera(screen)
clock = pygame.time.Clock()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    player.handlemovement(keys[K_w] or keys[K_UP],keys[K_s] or keys[K_DOWN],keys[K_a] or keys[K_LEFT],keys[K_d] or keys[K_RIGHT],tiles.colliders,camera)
    screen.fill((0,0,0))
    camera.rendergame(camera,player,tiles.colliders,tiles.floors)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()