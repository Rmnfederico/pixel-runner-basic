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

# Creating a font variable (for text surfaces)
test_font = pygame.font.Font('font/Pixeltype.ttf', 50) #(font_type, size)

# Creating a surface '.Surface((width, height))'
test_surface = pygame.Surface((100,200))
# Filling the surface with a color
test_surface.fill((255,0,0)) # can receive ('Color') as param.

# Creating a surface with an imported img / ALWAYS convert()
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
# Creating a font surface - (text, antialiasing, color)
text_surface = test_font.render('Halloo', False, 'Black')

# Creating a snail (enemy) surface
# - convert_alpha converts img AND alpha values (black/white stuff behind)
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
# Creating a constant var to modify snail_surface x position
snail_x_pos = 700

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

    # making snail_surf move left by decreasing x pos. value every loop 
    snail_x_pos -= 3
    # returning snail_surf to the right when x pos. reaches -60 value
    if snail_x_pos < -60: snail_x_pos = 800
    screen.blit(snail_surface, (snail_x_pos,265))

    # draw all our elements / update everything
    pygame.display.update()
    # limiting the FPS
    clock.tick(FPS)