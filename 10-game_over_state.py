import pygame
from sys import exit
pygame.init()

WIDTH, HEIGHT = 800, 400 
FPS = 60 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basics")
clock = pygame.time.Clock()

game_active = True

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
score_surface = test_font.render('My game', False, (64,64,64))
score_rect = score_surface.get_rect(center=(WIDTH/2,50))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(700,300))

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80,300))
PLAYER_GRAVITY = 0 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
        # Checking game_state before checking any player inputs
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                    PLAYER_GRAVITY = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    PLAYER_GRAVITY = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.x = 700
    
    # Nesting main game logic to check if game needs to finish
    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        pygame.draw.rect(screen,"#c0e8ec",score_rect) 
        pygame.draw.rect(screen,"#c0e8ec",score_rect.inflate(10,10),10,10) 
        screen.blit(score_surface, score_rect)

        snail_rect.x -= 5
        if snail_rect.right <= 0: snail_rect.left = 800
        screen.blit(snail_surface, snail_rect)

        # Player
        PLAYER_GRAVITY += 1
        player_rect.y += PLAYER_GRAVITY
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surface, player_rect)

        # Collision
        if snail_rect.colliderect(player_rect):
            # Switching game state to end 
            game_active = False
    else:
        screen.fill("Black")
        game_over_surf = test_font.render("Game Over", False, "Yellow")
        screen.blit(game_over_surf, game_over_surf.get_rect(center=(WIDTH/2, HEIGHT/2)))

    pygame.display.update()
    clock.tick(FPS)