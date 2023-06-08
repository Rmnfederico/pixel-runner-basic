import pygame
from sys import exit
from random import randint, choice
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80,300))
        self.gravity = 0

        # Importing sound (for jump)
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            # Implementing sound play with .play() method
            self.jump_sound.play().set_volume(0.01)
            self.gravity = -20
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        elif type == "snail":
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.type = type # USED BY ME TO CHANGE ANIMATION SPEED BY TYPE
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    def animation_state(self):
        if self.rect.x < 800:
            if self.type == "fly":
                self.animation_index += 0.3
            elif self.type == "snail":
                self.animation_index += 0.1

            if self.animation_index >= len(self.frames): self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]

    def move_object(self):
        self.rect.x -= 6
    
    def destroy_off_screen_obs(self):
        if self.rect.x <= -100:
            self.kill()

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

def check_sprite_collision():
    if pygame.sprite.spritecollide(player.sprite, obstacles_group, False):
        obstacles_group.empty()
        return False
    else: return True

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basics")
clock = pygame.time.Clock()

game_active = False
start_time = 0
score = 0
# Importing background music
bg_music = pygame.mixer.Sound("audio/music.wav")
# Setting sound volume (Must be done after creating the Sound object)
bg_music.set_volume(0.01)
# Playing music before game starts (so it doesn't bug)
bg_music.play(loops = -1) #loops at -1 = infinite looping

player = pygame.sprite.GroupSingle() #GroupSingle=group for a single spirte
player.add(Player())

obstacles_group = pygame.sprite.Group() 

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(WIDTH/2,HEIGHT/2))

title_surface = test_font.render("Pixel Runner", False, "Pink")
title_rect = title_surface.get_rect(midbottom=(WIDTH/2,player_stand_rect.y-50))

game_msg_surf = test_font.render(f"Press space to run", False, "Pink")
game_msg_rect = game_msg_surf.get_rect(center=(400,350))

obstacle_timer = pygame.USEREVENT + 1 # custom userevent (UE)
pygame.time.set_timer(obstacle_timer, 1500) #(event_to_trigger, how_often_ms)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
        if game_active:
            
            if event.type == obstacle_timer:
                obstacles_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        # Play background music when game starts
        #bg_music.play(loops= -1) #CANNOT PLAY IN THE LOOP
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))

        score = display_score()
        
        player.draw(screen)
        player.update()
        obstacles_group.draw(screen)
        obstacles_group.update()

        game_active = check_sprite_collision()

    else:
        screen.fill((94,139,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title_surface, title_rect)

        PLAYER_GRAVITY = 0

        score_message = test_font.render(f'Your score: {(score/1000):.1f}', False, "Pink")
        score_rect = score_message.get_rect(center= (400,330))
        
        if score > 0: screen.blit(score_message, score_rect)
        else: screen.blit(game_msg_surf, game_msg_rect)

    pygame.display.update()
    clock.tick(FPS)