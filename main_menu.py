import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Set the screen size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


# Set the window title
pygame.display.set_caption("Harry Potter Game")
icon = pygame.image.load('Harry_potter.png')
pygame.display.set_icon(icon)

background = pygame.image.load('castle.jpg')

mixer.music.load('background.wav')
mixer.music.play(-1)

# Create a font object for the start button
button_font = pygame.font.Font('freesansbold.ttf', 32)
start_button = button_font.render("START", True, (255, 255, 255))
start_button_rect = start_button.get_rect(center=(screen_width//2, screen_height//2))

#Pagrindinis menu
in_menu = True


# Game loop
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_button_rect.collidepoint(mouse_pos):
                # Start the game
                print("Starting game...")
                running = False
    
    # Fill the background with white
    screen.fill((0, 0, 0))
    #background image
    screen.blit(background,(0, 0))
    
    # Draw the start button on the screen
    pygame.draw.rect(screen, (0, 0, 0), start_button_rect)
    screen.blit(start_button, start_button_rect)
    
    # Update the display
    pygame.display.update()

# Quit pygame
pygame.quit()