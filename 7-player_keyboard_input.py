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

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
        # Checking if mouse is moving, inside event loop
        if event.type == pygame.MOUSEMOTION:
            # Checking if mouse pos. collides with player_rect
            if player_rect.collidepoint(event.pos):
                print(f"collision w/ mouse at {event.pos}")
        # Using event loop to check for key pressing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("jump")
        # Using event loop to check for key releasing
        if event.type == pygame.KEYUP:
            print("key up")

    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,300))
    pygame.draw.rect(screen,"#c0e8ec",score_rect) 

    pygame.draw.rect(screen,"#c0e8ec",score_rect.inflate(10,10),10,10) 
    screen.blit(score_surface, score_rect)

    snail_rect.x -= 3
    if snail_rect.right <= 0: snail_rect.left = 800
    screen.blit(snail_surface, snail_rect)
    screen.blit(player_surface, player_rect)

    # Get_pressed() returns an obj w/ all buttons & current state
    # keys = pygame.key.get_pressed() #storing keys obj. as a dict.
    # if keys[pygame.K_SPACE]:
    #     print('jump') 

    pygame.display.update()
    clock.tick(FPS)