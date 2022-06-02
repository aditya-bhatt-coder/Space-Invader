#importing modules
import pygame
#import random
import math

from pygame import mixer

#initializing modules
pygame.init()

#Creating Game Window
gameWindow = pygame.display.set_mode((800, 600))
#background image loading and scaling
bgImg = pygame.image.load("bg1.jpg")
bgImg = pygame.transform.scale(bgImg, (800,600))#.convert_alpha()

#Title and Icon of the game
pygame.display.set_caption("Space Attack")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

#Game specific variables
running = True
num_of_enemies = 10

#Score and font
score_value = 0
font = pygame.font.SysFont(None, 64)
#Score on Screen
def text_screen(text, color, x, y):
    screen_text  = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

#Player
playerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0
def player(x, y):
    gameWindow.blit(playerImg, (x, y))

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(10, 726))
    enemyY.append(random.randint(50, 175))
    enemyX_change.append(0.2)
    enemyY_change.append(40)
def enemy(x, y, i):
    gameWindow.blit(enemyImg[i], (x, y))

#Bullet
#ready - You can't see the bullet on screen
#Fire - The bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.8
bullet_state = "ready"
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    gameWindow.blit(bulletImg, (x+16, y+10))

#checking the collision between enemy and bullet
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

#Creating Game Loop
while running:
    #background image
    gameWindow.fill((0, 255, 255))
    gameWindow.blit(bgImg, (0, 0))
    
    #event loop starts
    for event in pygame.event.get():

        #to quit the game using X
        if event.type == pygame.QUIT:
            print("Quit")
            running = False

        #check if keystroke pressed or not
        if event.type == pygame.KEYDOWN:
            #cheat code using ctrl
            if event.key == pygame.K_RCTRL:
                score_value += 10
            #check left arrow key
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            #check right arrow key
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            #checking spacebar to fire the bullet
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    #gets the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        #check if keystroke released or not
        if event.type == pygame.KEYUP:
            #check left arrow key
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                playerX_change = 0
                
    #moving the spaceship according to the key pressed by changing the
    #x coordinate of the spaceship
    playerX += playerX_change

    #checking the margin for spaceship
    if playerX <= 10:
        playerX = 10
    elif playerX >=726:
        playerX = 726

    #Enemy Movement
    for i in range(num_of_enemies):
        #Game over
        if(enemyY[i] > 440):
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            text_screen("Game Over!!!", (255, 0, 0), 250, 250)
            break

        #moving the enemy according by changing its x-y coordinates
        enemyX[i] += enemyX_change[i]
        #checking the margin for enemy
        if enemyX[i] <= 10:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=726:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
        #checking collision between enemy and bullet
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            exp_Sound = mixer.Sound("explosion.wav")
            exp_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(10, 726)
            enemyY[i] = random.randint(50, 175)
        #calling func to display enemies on screen
        enemy(enemyX[i], enemyY[i], i)

    #Bullet Movement
    if bulletY <=0:     #for multiple bullets
        bulletY = 480
        bullet_state = "ready"
        
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        
    player(playerX, playerY)
    text_screen("Score : "+str(score_value), (255, 255, 255), 5, 5)
    pygame.display.update()
pygame.quit()
quit()
