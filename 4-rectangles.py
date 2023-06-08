import pygame
from sys import exit

pygame.init()

WIDTH, HEIGHT = 800, 400 
FPS = 60 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basics")
clock = pygame.time.Clock()

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

test_surface = pygame.Surface((100,200))
test_surface.fill((255,0,0))

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
text_surface = test_font.render('Halloo', False, 'Black')
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
# Creating snail's rectangle
snail_rect = snail_surface.get_rect(midbottom=(700,300))

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
# Creating player's rectangle off of player_surface (w/ get_rect())
#-get.rect() receives pos. to draw rect. as param. (topleft/center/midleft/bottomleft)
player_rect = player_surface.get_rect(midbottom=(80,300))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()

    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,300))
    screen.blit(text_surface, (350,50))

    # moving snail by its rectangle x pos (w/ '.x' attribute)
    snail_rect.x -= 3
    # using .left & .right rect. attributes to handle snail's pos.
    if snail_rect.right <= 0: snail_rect.left = 800
    screen.blit(snail_surface, snail_rect)

    # Blitting player_surface, in 'player_rect' position
    screen.blit(player_surface, player_rect)

    pygame.display.update()
    clock.tick(FPS)