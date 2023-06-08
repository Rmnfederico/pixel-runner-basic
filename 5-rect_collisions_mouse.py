import os
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
        # another way to get mouse pos.
        if event.type == pygame.MOUSEMOTION:
            #getting mouse pos.(x,y) through the event 
            #print(event.pos)
            if player_rect.collidepoint(event.pos):
                print(f"collision at {event.pos}")
            
        # checking if mouse buttons are clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("mouse click down")
        # checking if mouse click is released
        if event.type == pygame.MOUSEBUTTONUP:
            print("mouse click released")

    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,300))
    screen.blit(text_surface, (350,50))

    snail_rect.x -= 3
    if snail_rect.right <= 0: snail_rect.left = 800
    screen.blit(snail_surface, snail_rect)
    screen.blit(player_surface, player_rect)

    # using colliderect() to check collition between 2 rects.
    # if player_rect.colliderect(snail_rect):
    #     player_rect.y -= 3
    # elif snail_rect.right < player_rect.left:
    #     if player_rect.bottom < 300:
    #         player_rect.bottom += 3

    # saving (x,y) mouse pos. as a tuple with .get_pos()
    mouse_pos = pygame.mouse.get_pos()
    
    # using collidepoint() to check if player rect is colliding with mouse pos.
    if player_rect.collidepoint(mouse_pos): #collidepoint((tuple=x,y))
        #print("colission")
        #get_pressed() checks if any mouse button is pressed
        #print(pygame.mouse.get_pressed())
        pass
    else:
        #os.system('cls')
        pass
    

    pygame.display.update()
    clock.tick(FPS)