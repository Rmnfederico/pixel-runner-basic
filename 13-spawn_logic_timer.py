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

# Creating Obstacle movement function (handle obstacles movement)
def obstacle_movement(obstacle_list):
    if obstacle_list:
        #if list is not empty, move obstacles rects. inside left in x axis
        for obs_rect in obstacle_list:
            obs_rect.x -= 5
            
            #using snail y bottom pos. to know when to blit a fly or snail
            if obs_rect.bottom == 300: screen.blit(snail_surface, obs_rect)
            else: screen.blit(fly_surface, obs_rect)
            
        
        #using list comprehension to delete obstacles too far to the left
        obstacle_list = [obs for obs in obstacle_list if obs.x > -100]

        #returning the list to surpass local scope problem
        return obstacle_list
    #if no elements in the list, return an empty list to avoid returning None
    else: return []

# Re-implementing collition for obstacles_rects_list w/ player
def check_collition(player: pygame.Rect, obstacles):
    if obstacles:
        #looping obstacles rects list to check for collision w/ player
        for obs_rect in obstacles:
            #if pygame.sprite.collide_rect(player, obs_rect):
            if player.colliderect(obs_rect):
                # if collided, return False to change game_active var
                return False
    #if no collision happened, return True to game_active var
    return True

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basics")
clock = pygame.time.Clock()

game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# Obstacles
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()

# creating fly obstacle
fly_surface = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()

# creating a list to store obstacles, displace them and erase them after
obstacle_rect_list = []


player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80,300))
PLAYER_GRAVITY = 0 

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(WIDTH/2,HEIGHT/2))

title_surface = test_font.render("Pixel Runner", False, "Pink")
title_rect = title_surface.get_rect(midbottom=(WIDTH/2,player_stand_rect.y-50))

game_msg_surf = test_font.render(f"Press space to run", False, "Pink")
game_msg_rect = game_msg_surf.get_rect(center=(400,350))

# Implementing Timer

#pygame reserves some events, so add +1 to any custom UE to avoid conflicts
obstacle_timer = pygame.USEREVENT + 1 # custom userevent (UE)

# Setting an interval to trigger custom every every certain time (ms)
pygame.time.set_timer(obstacle_timer, 1500) #(event_to_trigger, how_often_ms)

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
            
            #Adding custom event created to event loop
            if event.type == obstacle_timer:
                #using random generated ints to spawn(append) either a fly or a snail
                if randint(0,2):
                    #Appending snails obstacles to the list, with a random X value to te right
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900,1100),210)))
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
        screen.blit(player_surface, player_rect)

        # Implementing Obstacle movement function
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Checking collision w/ objects to change game state to False
        game_active = check_collition(player_rect, obstacle_rect_list)

    else:
        screen.fill((94,139,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title_surface, title_rect)

        #Emptying obstacles list if game ends (to 'reset' it)
        obstacle_rect_list.clear()
        #Placing player at starting pos. again when game ended
        player_rect.midbottom = (80,300)
        #Resetting gravity value as well
        PLAYER_GRAVITY = 0

        score_message = test_font.render(f'Your score: {(score/1000):.1f}', False, "Pink")
        score_rect = score_message.get_rect(center= (400,330))
        
        if score > 0: screen.blit(score_message, score_rect)
        else: screen.blit(game_msg_surf, game_msg_rect)

    pygame.display.update()
    clock.tick(FPS)