import pygame
import math
import random
from pygame import mixer

#initialize the pygame
pygame.init()

#create the screen, Define screen size
screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Hogwarts Game")

#Background
background = pygame.image.load('castle.jpg')

#initialize the pygame mixer
pygame.mixer.init()

#Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#title and icon
pygame.display.set_caption("Hogwarts Invaders")
icon = pygame.image.load('Harry_potter.png')
pygame.display.set_icon(icon)

#Potter
playerImg = pygame.image.load('Harry_potter.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

#Levels
level = 1

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10
enemy_row = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('voldemort2.png'))
    enemyX.append(64 + (i % 10) * 64)
    enemyY.append(70 + (i // enemy_row) * 64)
    enemyX_change.append(0.1)
    enemyY_change.append(0.05)

#Avada
#ready - you cant see the spell on the screen
#fire - the spell is currently moving
bulletImg = pygame.image.load('spell.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready"

#score
score_value = 0
total_score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#Game over text
over_font = pygame.font.Font('freesansbold.ttf',64)
in_menu = True

def show_score(x, y):
    score = font.render("Score :" + str(score_value) + "   Total Score: " + str(total_score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY - bulletY,2)))
    if distance < 35:
        return True
    else:
        return False
    
def countdown_timer():
    start_ticks = pygame.time.get_ticks()  # Get the current time in milliseconds
    while True:
        # Calculate the remaining time in seconds
        remaining_time = 5 - (pygame.time.get_ticks() - start_ticks) / 1000
        if remaining_time <= 0:
            break  # Exit the loop when the countdown is over
        
        # Display the remaining time on the screen
        countdown_font = pygame.font.Font('freesansbold.ttf', 32)
        countdown_text = countdown_font.render("Next level in " + str(int(remaining_time)) + " seconds", False, (255, 255, 255))
        # fill the screen with a solid color to erase the previous time display
        screen.fill((0, 0, 0))
        screen.blit(countdown_text, (200, 250))
        pygame.display.update()

#game loop
running = True
while running:
    # RGB - screen colour
    screen.fill((0, 0, 0))
    #background image
    screen.blit(background,(0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('reducto.wav')
                    bullet_Sound.set_volume(0.2)
                    bullet_Sound.play()
                    #get the current x coordinate of the Harrypotter
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    #checking for boundaries for potter so it doesn't go out of boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #Enemy movement
    for i in range(num_of_enemies):

    #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                    enemyY[j] = 2000
            game_over_text()
            break

        enemyY[i] += enemyY_change[i]
        if enemyY[i] >= 536:
            enemyY[i] = -64
            enemyX[i] = random.randint(0, 736)
        enemy(enemyX[i], enemyY[i], i)

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('hit.wav')
            explosion_Sound.set_volume(0.3)
            explosion_Sound.play()
            bulletY = 400
            bullet_state = "ready"
            score_value += 1
            total_score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        # Check if the player has reached a new level
        if score_value == 10 * level:
            level += 1
            score_value = 0 # Reset the score to 0
            num_of_enemies += 10
            for i in range(num_of_enemies - 10, num_of_enemies):
                enemyImg.append(pygame.image.load('voldemort2.png'))
                enemyX.append(64 + (i % 10) * 64)
                enemyY.append(70 + (i // enemy_row) * 64)
                enemyX_change.append(0.1 + 0.01 * level)  # Increase the X speed by 0.01 for each level
                enemyY_change.append(0.05 + 0.01 * level)  # Increase the Y speed by 0.01 for each level
            countdown_timer()
            for j in range(num_of_enemies):
                enemyY[j] = -64  # Reset the Y position of all enemies

    #Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
