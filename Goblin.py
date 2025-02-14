import sys, math, pygame

width = 1024
height = 720

pygame.init()
window = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
while True:
    pygame.event.get()
    clock.tick(60)
