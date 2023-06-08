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
score_surface = test_font.render('My game', False, (64,64,64))
#using a rectangle to center score to mid screen (using WIDTH/2)
score_rect = score_surface.get_rect(center=(WIDTH/2,50))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(700,300))

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
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
    #drawing rectangle w/ draw.rect(dest_surf, color, source_rect)
    pygame.draw.rect(screen,"#c0e8ec",score_rect) 
    
    #using .inflate() method to enlarge score_rect size
    #rounding borders with 'border_radius' draw.rect()'s param.
    pygame.draw.rect(screen,"#c0e8ec",score_rect.inflate(10,10),10,10) 
    screen.blit(score_surface, score_rect)

    #drawing a line - (dest_surf, color, start_pos, end_pos, width)
    #pygame.draw.line(screen, "Yellow", (0,400),(800,0),10)
    #using mouse.get_pos() as end_pos, so line follows mouse
    #pygame.draw.line(screen, "Yellow", (0,400),pygame.mouse.get_pos(),10)

    #drawing a circle
    #pygame.draw.ellipse(screen, "Brown", pygame.Rect(50,200,100,100))

    snail_rect.x -= 3
    if snail_rect.right <= 0: snail_rect.left = 800
    screen.blit(snail_surface, snail_rect)
    screen.blit(player_surface, player_rect)

    pygame.display.update()
    clock.tick(FPS)
