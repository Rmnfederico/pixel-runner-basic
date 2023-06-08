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
score_rect = score_surface.get_rect(center=(WIDTH/2,50))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(700,300))

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80,300))

# Creating an initial gravity value
PLAYER_GRAVITY = 0 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Using mouse buttons clicked over player to jump
            if player_rect.collidepoint(event.pos):
                PLAYER_GRAVITY = -20

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Using gravity to create a jump state
                PLAYER_GRAVITY = -20

    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,300))
    pygame.draw.rect(screen,"#c0e8ec",score_rect) 

    pygame.draw.rect(screen,"#c0e8ec",score_rect.inflate(10,10),10,10) 
    screen.blit(score_surface, score_rect)

    snail_rect.x -= 3
    if snail_rect.right <= 0: snail_rect.left = 800
    screen.blit(snail_surface, snail_rect)

    # Player

    # Increasing player_gravity every single loop
    PLAYER_GRAVITY += 1
    # Adding increasing gravity value to y pos. to make player 'fall'
    player_rect.y += PLAYER_GRAVITY
    screen.blit(player_surface, player_rect)

    pygame.display.update()
    clock.tick(FPS)