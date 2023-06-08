import pygame
from sys import exit

pygame.init()

# Setting constants 
WIDTH, HEIGHT = 800, 400 #(set_mode receives this as a tuple)
FPS = 60 #clock obj receives this as .tick() method param.

# Creating a display surface (stored in a variable)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Setting a title
pygame.display.set_caption("Basics")

# Setting a clock object to limit FPS
clock = pygame.time.Clock()

# Creating a font variable w/ imported font(for text surfaces)
test_font = pygame.font.Font('font/Pixeltype.ttf', 50) #(font_type, size)

# Creating a font variable from a system font
sys_font = pygame.font.SysFont("Arial Narrow", 50)

# Creating a surface '.Surface((width, height))'
test_surface = pygame.Surface((100,200))
# Filling the surface with a color
test_surface.fill((255,0,0)) # can receive ('Color') as param.

# Creating a surface with an imported img
sky_surface = pygame.image.load('graphics/Sky.png')
ground_surface = pygame.image.load('graphics/ground.png')
# Creating a font surface - (text, antialiasing, color)
text_surface = test_font.render('Halloo', False, 'Black')

running = True
while running:
    #setting for loop to 'liste' for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit() #needed to avoid 'pygame.error:video system not initialized'

    # attaching a surface to the screen (display surface)
    screen.blit(sky_surface, (0,0)) #blit = block image transfer
    screen.blit(ground_surface, (0,300))
    screen.blit(text_surface, (350,50))

    # draw all our elements / update everything
    pygame.display.update()
    # limiting the FPS
    clock.tick(FPS)