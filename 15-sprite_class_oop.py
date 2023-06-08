import pygame
from sys import exit
from random import randint, choice
pygame.init()

# Ceating Player Class (inherits from sprite class)
class Player(pygame.sprite.Sprite):
    #creating player constructor
    def __init__(self):
        #initializing sprite class constructor to access it from Player
        super().__init__()
        
        # Setting attributes
        # Building surfs. & surfs. list for animation, inside constructor

        #importing player walk frames as surfaces
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        #placing frames inside player walk frames list (w/ self to access them outside init method) 
        self.player_walk = [player_walk_1, player_walk_2]
        #player index w/ self (needs to be available on the entire class)
        self.player_index = 0
        #importing player_jump frame(.png) as surface (w/ self also)
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        #setting first index of player frames list as self.image by default
        self.image = self.player_walk[self.player_index]
        #setting rectangle to place surface on screen
        self.rect = self.image.get_rect(midbottom=(80,300))
        #setting gravity to handle fall speed (0 by default)
        self.gravity = 0

    #recreating player imputs (before implemented on event loop)
    def player_input(self):
        #get all keys w/ get_pressed
        keys = pygame.key.get_pressed()
        #recreating jump login through self.gravity attribute
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
    def apply_gravity(self):
        #increasing gravity value every loop
        self.gravity += 1
        #adding gravity value to player y pos. every loop (so it adds up)
        self.rect.y += self.gravity
        #avoiding player to go below 300 on y axis (so it doesnt fall off screen)
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    # Building animation inside class (replicating player_animation() func)
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    # Sprites 2 main methods = draw() & update()

    # Implemeting update() to match sprite group's update() (READ SNIPPET)
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

# Creating obstacle Class w/ sprite class inherited
class Obstacle(pygame.sprite.Sprite):
    #constructor receives 'type' as well (fly or snail)
    def __init__(self, type):
        #initializing sprite class constructor to access it here
        super().__init__()
        # logic to save a list of surfs depending on the type argument
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            #setting y position for the fly
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            #setting y position for the snail
            y_pos = 300

        # Setting attributes (image & rect atts. ALWAYS NEEDED)
        self.type = type # USED BY ME TO CHANGE ANIMATION SPEED BY TYPE
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    # Implementing animation
    def animation_state(self):
        if self.rect.x < 800:
            # implement animation according to type
            if self.type == "fly":
                self.animation_index += 0.3
            elif self.type == "snail":
                self.animation_index += 0.1

            if self.animation_index >= len(self.frames): self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]

    def move_object(self):
        self.rect.x -= 6
    
    # Implementing method to destro off screen obstacles
    def destroy_off_screen_obs(self):
        if self.rect.x <= -100:
            #removing the sprite for all group w/ .kill() sprite method
            self.kill()

    # Creating update() method to use it with the sprite group's method
    def update(self):
        self.animation_state()
        self.move_object()
        self.destroy_off_screen_obs()

WIDTH, HEIGHT = 800, 400 
FPS = 60 

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surface = test_font.render(f'Score:{(current_time/1000):.1f}', False, (64,64,64))
    score_rect = score_surface.get_rect(center= ((400,50)))
    screen.blit(score_surface, score_rect)
    return current_time

# def obstacle_movement(obstacle_list):
#     if obstacle_list:
#         for obs_rect in obstacle_list:
#             obs_rect.x -= 5
            
#             if obs_rect.bottom == 300: screen.blit(snail_surface, obs_rect)
#             else: screen.blit(fly_surface, obs_rect)

#         obstacle_list = [obs for obs in obstacle_list if obs.x > -100]

#         return obstacle_list
#     else: return []

def check_collition(player: pygame.Rect, obstacles):
    if obstacles:
        for obs_rect in obstacles:
            if player.colliderect(obs_rect):
                return False
    return True

def check_sprite_collision():
    #spritecollide() returns a list of sprites that collide between a group and a sprite
    if pygame.sprite.spritecollide(player.sprite, obstacles_group, False):
        #if collision, remove all obstacles sprites before game restart
        obstacles_group.empty()
        #False if the list is not empty (thus collision happened)
        return False
    else: return True

# def player_animation():
#     global player_surface, player_index
#     if player_rect.bottom < 300:
#         player_surface = player_jump
#     else:
#         player_index += 0.1
#         if player_index >= len(player_walk): player_index = 0
#         player_surface = player_walk[int(player_index)]



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basics")
clock = pygame.time.Clock()

game_active = False
start_time = 0
score = 0

# Groups (player & obstacles)

# Creating a GrouSingle to contain ONLY the player sprite
player = pygame.sprite.GroupSingle() #GroupSingle=group for a single spirte
# Adding an instance of the player to the GroupSingle
player.add(Player())

# Creating a regular group to contain obstacles sprites
obstacles_group = pygame.sprite.Group() 
#NOTE: obstacles will be added with .add() in the event loop through of obstacles timer user event

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
# snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()

# snail_frames = [snail_frame_1, snail_frame_2]
# snaiL_frame_index = 0
# snail_surface = snail_frames[snaiL_frame_index]

# fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
# fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
# fly_frames = [fly_frame_1, fly_frame_2]
# fly_frame_index = 0
# fly_surface = fly_frames[fly_frame_index]

# obstacle_rect_list = []

# player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
# player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()

# player_walk = [player_walk_1, player_walk_2]

# player_index = 0

# player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

# player_surface = player_walk[player_index]

# player_rect = player_surface.get_rect(midbottom=(80,300))
#PLAYER_GRAVITY = 0 

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(WIDTH/2,HEIGHT/2))

title_surface = test_font.render("Pixel Runner", False, "Pink")
title_rect = title_surface.get_rect(midbottom=(WIDTH/2,player_stand_rect.y-50))

game_msg_surf = test_font.render(f"Press space to run", False, "Pink")
game_msg_rect = game_msg_surf.get_rect(center=(400,350))

obstacle_timer = pygame.USEREVENT + 1 # custom userevent (UE)
pygame.time.set_timer(obstacle_timer, 1500) #(event_to_trigger, how_often_ms)

# snail_animation_timer = pygame.USEREVENT + 2
# pygame.time.set_timer(snail_animation_timer, 500) #triggers ever 500 ms.

# fly_animation_timer = pygame.USEREVENT + 3
# pygame.time.set_timer(fly_animation_timer, 200) #triggers ever 200 ms.

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
        if game_active:
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
            #         PLAYER_GRAVITY = -20
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE and player_rect.bottom == 300:
            #         PLAYER_GRAVITY = -20
            
            if event.type == obstacle_timer:
                # Adding an instance of Obstacle to the obstacles group
                #NOTE:using 'choice' method to add a fly or snail, by percentage
                obstacles_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))
                #if randint(0,2): obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900,1100),300)))
                #else: obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900,1100),210)))
        
            # if event.type == snail_animation_timer:
            #     if snaiL_frame_index == 0:
            #         snaiL_frame_index = 1
            #     else:
            #         snaiL_frame_index = 0
            #     snail_surface = snail_frames[snaiL_frame_index]
            # if event.type == fly_animation_timer:  
            #     if fly_frame_index == 0:
            #         fly_frame_index = 1
            #     else:
            #         fly_frame_index = 0
            #     fly_surface = fly_frames[fly_frame_index]
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))

        score = display_score()

        # Player
        # PLAYER_GRAVITY += 1
        # player_rect.y += PLAYER_GRAVITY
        # if player_rect.bottom >= 300: player_rect.bottom = 300

        # player_animation()
        # screen.blit(player_surface, player_rect)
        
        # Drawing player SPRITE group on screen w/ draw(surface) 
        player.draw(screen)
        # Calling the update() method inside Player class
        player.update()
        # Drawing obstacles SPRITE group in the screen
        obstacles_group.draw(screen)
        # Calling the update() method inside Obstacle class
        obstacles_group.update()

        #obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Using new collition sprite method to handle game state
        game_active = check_sprite_collision()

    else:
        screen.fill((94,139,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title_surface, title_rect)

        #obstacle_rect_list.clear()
        #player_rect.midbottom = (80,300)
        PLAYER_GRAVITY = 0

        score_message = test_font.render(f'Your score: {(score/1000):.1f}', False, "Pink")
        score_rect = score_message.get_rect(center= (400,330))
        
        if score > 0: screen.blit(score_message, score_rect)
        else: screen.blit(game_msg_surf, game_msg_rect)

    pygame.display.update()
    clock.tick(FPS)