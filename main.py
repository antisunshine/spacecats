import pygame
import random
import math
from pygame import mixer

# Initialise the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("img/background.png")

# Background sound
mixer.music.load('sounds/metal.ogg')
mixer.music.play(-1)
mixer.music.set_volume(0.5)

# Tittle and Icons
pygame.display.set_caption("SpaceCat Invaders")
icon = pygame.image.load("img/alien.png")
playerIcon = pygame.image.load("img/cat.png")
bulletIcon = pygame.image.load("img/thread.png")
pygame.display.set_icon(icon)

# Player
playerX = 379
playerY = 480
playerX_change = 0

# Enemy
enemyIcon = []
enemyX = []
enemyY = []
enemyX_change = 1
enemyY_change = 30
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyIcon.append(pygame.image.load("img/mouse.png"))
    enemyX.append(random.randint(50, 735))
    enemyY.append(random.randint(50, 150))

# Bullet
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('fonts/ActionComics.ttf', 32)

textX = 10
textY = 10

# Game Over
overFont = pygame.font.Font('fonts/ActionComics.ttf', 64)


def showScore(x, y):
    score = font.render(str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def gameOver():
    overText = overFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overText, (50, 250))


def player(x, y):
    screen.blit(playerIcon, (x, y))


def enemy(x, y, k):
    screen.blit(enemyIcon[k], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIcon, (x + 16, y + 10))


def isCollision(eneX, eneY, bullX, bullY):
    # Formula for the calculation of the distance of two points
    distance = math.sqrt((math.pow(eneX - bullX, 2)) + (math.pow(eneY - bullY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True

while running:
    for event in pygame.event.get():
        # Exit check
        if event.type == pygame.QUIT:
            running = False
        # Event controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound('sounds/ka-pew.wav')
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Screen color
    screen.fill((128, 128, 128))
    # Background image
    screen.blit(background, (0, 0))

    # Player boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # Call Player
    player(playerX, playerY)

    # Enemy boundaries and movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change
        if enemyX[i] <= 0:
            enemyX_change = 1
            for j in range(num_of_enemies):
                enemyY[j] += enemyY_change
        elif enemyX[i] >= 736:
            enemyX_change = -1
            for j in range(num_of_enemies):
                enemyY[j] += enemyY_change
        if enemyY[i] > 410:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            gameOver()
            break

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            hitSound = mixer.Sound('sounds/rat.ogg')
            hitSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 100
            enemyX[i] = random.randint(50, 750)
            enemyY[i] = random.randint(50, 150)

        # Call enemy
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Score
    showScore(textX, textY)

    # Update screen
    pygame.display.update()
