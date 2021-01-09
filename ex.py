import pygame
import random
import math
from pygame import mixer

# Initialise the pygame
pygame.init()

# Screen wdth and screen height
screen_width = 800
screen_height = 600
# Create the screen
screen = pygame.display.set_mode((screen_width,screen_height))
running = True

# Score
score = 0

# To display the score
scoreX = 10
scoreY = 10
font = pygame.font.Font("freesansbold.ttf",22)

# Tile and Logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player1.png")
playerX = screen_width//2 - 25
playerY = screen_height - 75
speed = 4

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = playerX + 13
bulletY = playerY - 10
fire = False
bullet_state = "ready"
bullet_speed = 5

# Enimies
no_of_enemies = 6
enemyImg = []
enemyX = []
enemyY = []
movex = []

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,screen_width - 40))
    enemyY.append(random.randint(50,screen_height//3))
    movex.append(4)

# Enemy
# enemyImg = pygame.image.load("enemy.png")
# enemyX = random.randint(0,screen_width - 40)
# enemyY = random.randint(50,screen_height//3)
# movex = 4

# Background
backgroundImg = pygame.image.load("background.jpg")

# Background Music
mixer.music.load("Battleship.ogg")
mixer.music.play(-1)

def player(x,y):
    screen.blit(playerImg,(x,y))


def enemy(x,y,i):
    screen.blit(enemyImg[i],(x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+13,y))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow((enemyY-bulletY),2))
    return  distance < 18

def display_score(x,y):
    z = font.render("Score: "+str(score),True,(255,255,255))
    screen.blit(z,(x,y))
# Infinite runnning Game Loop
while running:
    # RGB = Red Green Blue
    screen.fill((0,0,0))
    screen.blit(backgroundImg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Enemy Movement
    for i in range(no_of_enemies):
        enemyX[i] += movex[i]
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyY[i] += 10
            movex[i] = 4
        if enemyX[i] >= screen_width - 50:
            enemyX[i] = screen_width - 50
            enemyY[i] += 10
            movex[i] = -4
        
        # Enemy added to the screen
        enemy(enemyX[i],enemyY[i],i)
        
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("Explosion.wav")
            explosion_sound.play()
            bulletY = playerY - 10
            bullet_state = "ready"
            enemyX[i] = random.randint(0, screen_width - 40)
            enemyY[i] = random.randint(50, screen_height//3)
            score += 1

    # If key Stroke is pressed check whether it is right or left
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX -= speed
        if event.key == pygame.K_RIGHT:
            playerX += speed
        if event.key == pygame.K_SPACE:
            cannon_sound = mixer.Sound("awm.wav")
            cannon_sound.play()
            bulletX = playerX
            fire_bullet(bulletX,bulletY)
        if playerX < 0:
            playerX = 0
        if playerX >= screen_width - 50:
            playerX = screen_width - 50

    # Player added to the screen
    player(playerX,playerY)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = playerY - 10
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bullet_speed

    display_score(scoreX,scoreY)

    # Game Over
    for i in range(no_of_enemies):    
        if enemyY[i] > screen_height - 100:
            screen.fill((0,0,0))
            text = pygame.font.Font("freesansbold.ttf",50)
            game_over = text.render("Game Over",True,(255,255,255))
            screen.blit(game_over,(300,250))
            z = pygame.font.Font("freesansbold.ttf",40)
            score_text = z.render("Score: "+str(score),True,(255,255,255))
            screen.blit(score_text,(358,300))
            exit()

    pygame.display.update()