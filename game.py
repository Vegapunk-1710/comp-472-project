import sys
import pygame
from settings import Settings
from grid import Grid

pygame.init()
pygame.font.init()
grid = Grid()
display = pygame.display.set_mode(Settings.WINDOW_SIZE)
pygame.display.set_caption("Wargame 💣")
clock = pygame.time.Clock()
done = False

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            grid.update(pos)


    display.fill(Settings.BLACK)
    grid.render(display)


    clock.tick(60)
    pygame.display.flip()


pygame.quit()