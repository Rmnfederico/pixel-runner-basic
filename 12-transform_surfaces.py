import pygame
from sys import exit
pygame.init()

WIDTH, HEIGHT = 800, 400 
FPS = 60 

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surface = test_font.render(f'Score:{(current_time/1000):.1f}', False, (64,64,64))
    score_rect = score_surface.get_rect(center= ((400,50)))
    screen.blit(score_surface, score_rect)
    # returning current_time to save the score and display it
    return current_time

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basics")
clock = pygame.time.Clock()

game_active = False
start_time = 0
# Initializing score var to save score and display it 
score = 0

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(700,300))

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80,300))
PLAYER_GRAVITY = 0 

# Creating player_stand scaled surface for Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
# using rotozoom to scale, rotate and smoothen the img
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(WIDTH/2,HEIGHT/2))

# Creating title for intro screen
title_surface = test_font.render("Pixel Runner", False, "Pink")
title_rect = title_surface.get_rect(midbottom=(WIDTH/2,player_stand_rect.y-50))

# Creating game intro/over + final score msg for intro screen
game_msg_surf = test_font.render(f"Press space to run", False, "Pink")
game_msg_rect = game_msg_surf.get_rect(center=(400,350))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
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
                start_time = pygame.time.get_ticks()
    
    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))

        # Storing score to the created var to display it after
        score = display_score()

        snail_rect.x -= 5
        if snail_rect.right <= 0: snail_rect.left = 800
        screen.blit(snail_surface, snail_rect)

        # Player
        PLAYER_GRAVITY += 1
        player_rect.y += PLAYER_GRAVITY
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surface, player_rect)

        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill((94,139,162))
        # Blitting player and title for intro screen
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title_surface, title_rect)
        
        #Creating score msg. surf. and rect.
        score_message = test_font.render(f'Your score: {(score/1000):.1f}', False, "Pink")
        score_rect = score_message.get_rect(center= (400,330))
        
        # If game started and score surpassed 0, blit score_msg
        if score > 0: screen.blit(score_message, score_rect)
        else: screen.blit(game_msg_surf, game_msg_rect)

    pygame.display.update()
    clock.tick(FPS)