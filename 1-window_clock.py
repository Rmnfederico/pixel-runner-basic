import pygame
from sys import exit

pygame.init()

WIDTH, HEIGHT = 800, 400 #(set_mode receives this as a tuple)
FPS = 60 #clock obj receives this as .tick() method param.
# Creating a display surface (stored in a variable)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Setting a title
pygame.display.set_caption("Basics")

# Setting a clock object to limit FPS
clock = pygame.time.Clock()

running = True
while running:
    #setting for loop to 'liste' for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit() #needed to avoid 'pygame.error:video system not initialized'

    # draw all our elements / update everything
    pygame.display.update()
    # limiting the FPS
    clock.tick(FPS)