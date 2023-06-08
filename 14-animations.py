import pygame
from sys import exit
from random import randint
pygame.init()

WIDTH, HEIGHT = 800, 400 
FPS = 60 

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surface = test_font.render(f'Score:{(current_time/1000):.1f}', False, (64,64,64))
    score_rect = score_surface.get_rect(center= ((400,50)))
    screen.blit(score_surface, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obs_rect in obstacle_list:
            obs_rect.x -= 5
            
            if obs_rect.bottom == 300: screen.blit(snail_surface, obs_rect)
            else: screen.blit(fly_surface, obs_rect)

        obstacle_list = [obs for obs in obstacle_list if obs.x > -100]

        return obstacle_list
    else: return []

def check_collition(player: pygame.Rect, obstacles):
    if obstacles:
        for obs_rect in obstacles:
            if player.colliderect(obs_rect):
                return False
    return True

def player_animation():
    #declaring 2 global vars to overwirte player_surface / save an index
    global player_surface, player_index
    #if player's bottom is not at ground level(height), animate jump
    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        #index starts at 0 (walk_1 surf) and increments by 0.1 so 
        #it takes some frames to reach 1 (next index) and change animation
        player_index += 0.1
        # forcing index to turn 0 so it only iterates over valid indexes
        if player_index >= len(player_walk): player_index = 0
        # using the incremented index to iterate between animations
        # casted as int() b/c indexes can only be integers
        player_surface = player_walk[int(player_index)]



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basics")
clock = pygame.time.Clock()

game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# Importing snails/flies pngs as surfaces to build objects animations
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()

# Doing the same as done w/ player, creating a list w/ the png surfs.,
# setting an initial surf index to 0 & saving list 1rst index as obj_surf
snail_frames = [snail_frame_1, snail_frame_2]
snaiL_frame_index = 0
snail_surface = snail_frames[snaiL_frame_index]

# Same process than snail and player:
# png surfs. -> surfs list -> index=0 -> obj_surf=list[index=0]
fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []

# Saving separate player .pngs to surfaces to build the animation
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()

# Creating a list of player pngs
player_walk = [player_walk_1, player_walk_2]

# Creating an index to pick a surface from player_walk surfaces list
player_index = 0

# Importing player jump png as surface
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

# Initializing player_surface as the first surface of player surfs. list
player_surface = player_walk[player_index]

player_rect = player_surface.get_rect(midbottom=(80,300))
PLAYER_GRAVITY = 0 

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(WIDTH/2,HEIGHT/2))

title_surface = test_font.render("Pixel Runner", False, "Pink")
title_rect = title_surface.get_rect(midbottom=(WIDTH/2,player_stand_rect.y-50))

game_msg_surf = test_font.render(f"Press space to run", False, "Pink")
game_msg_rect = game_msg_surf.get_rect(center=(400,350))

obstacle_timer = pygame.USEREVENT + 1 # custom userevent (UE)
pygame.time.set_timer(obstacle_timer, 1500) #(event_to_trigger, how_often_ms)

# Creating user events & timers to animate the objects when triggered
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500) #triggers ever 500 ms.

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200) #triggers ever 200 ms.

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
            
            if event.type == obstacle_timer:
                if randint(0,2): obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900,1100),300)))
                else: obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900,1100),210)))
        
            # Implementing user events logic for snails animations
            if event.type == snail_animation_timer:
                #swapping between sprites when event timer triggers
                if snaiL_frame_index == 0:
                    # using surfs list index to swap
                    snaiL_frame_index = 1
                else:
                    # using surfs list index to swap
                    snaiL_frame_index = 0
                # finally saving the selected surf. to blit it later
                snail_surface = snail_frames[snaiL_frame_index]
            # Implementing user events logic for flies animations
            if event.type == fly_animation_timer:  
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))

        score = display_score()

        # Player
        PLAYER_GRAVITY += 1
        player_rect.y += PLAYER_GRAVITY
        if player_rect.bottom >= 300: player_rect.bottom = 300

        # Calling player_animation func. before blitting player
        player_animation()

        screen.blit(player_surface, player_rect)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        game_active = check_collition(player_rect, obstacle_rect_list)

    else:
        screen.fill((94,139,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title_surface, title_rect)

        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        PLAYER_GRAVITY = 0

        score_message = test_font.render(f'Your score: {(score/1000):.1f}', False, "Pink")
        score_rect = score_message.get_rect(center= (400,330))
        
        if score > 0: screen.blit(score_message, score_rect)
        else: screen.blit(game_msg_surf, game_msg_rect)

    pygame.display.update()
    clock.tick(FPS)