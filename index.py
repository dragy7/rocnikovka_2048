import pygame
pygame.init()


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2048")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:  
                down = True
            if event.type == pygame.K_UP:   
                up = True
            if event.type == pygame.K_LEFT: 
                left = True
            if event.type == pygame.K_RIGHT:    
                right = True
            



