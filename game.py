from pygame import mixer
import random
import math
from menu import *


class Game:
    def __init__(self):
        pygame.init()

        # key controls
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.L_KEY, self.R_KEY, self.SPACE_KEY = False, False, False, False, False, False, False

        # display settings
        pygame.display.set_caption("SpaceCat Invaders")
        self.icon = pygame.image.load("img/alien.png")
        pygame.display.set_icon(self.icon)
        self.DISPLAY_W, self.DISPLAY_H = 800, 600
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.fontName = "fonts/ActionComics.ttf"
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.mainMenu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curMenu = self.mainMenu

        # images
        self.bg = pygame.image.load("img/background.png")

        # sounds
        mixer.music.load('sounds/metal.ogg')
        mixer.music.play(-1)
        mixer.music.set_volume(0.5)

        # player
        self.playerIcon = pygame.image.load("img/cat.png")
        self.playerX = 379
        self.playerY = 480
        self.playerX_change = 0

        # bullet
        self.bulletIcon = pygame.image.load("img/thread.png")
        self.bulletX = 0
        self.bulletY = 480
        self.bulletX_change = 0
        self.bulletY_change = 10
        self.bulletState = "ready"

        # enemy
        self.enemyIcon = []
        self.enemyX = []
        self.enemyY = []
        self.enemyX_change = 1
        self.enemyY_change = 30
        self.num_of_enemies = 6

        for i in range(self.num_of_enemies):
            self.enemyIcon.append(pygame.image.load("img/mouse.png"))
            self.enemyX.append(random.randint(50, 735))
            self.enemyY.append(random.randint(50, 150))

        # Score
        self.score = 0

        self.textX = 10
        self.textY = 10

        # Game Over
        self.overFont = pygame.font.Font('fonts/ActionComics.ttf', 64)

    def gameLoop(self):
        while self.playing:
            self.checkEvents()
            if self.START_KEY:
                self.playing = False
            self.display.fill(self.BLACK)
            self.display.blit(self.bg, (0, 0))

            # Player
            if self.L_KEY:
                self.playerX -= 2
            if self.R_KEY:
                self.playerX += 2
            # Player boundaries
            self.playerX += self.playerX_change
            if self.playerX <= 0:
                self.playerX = 0
            elif self.playerX >= 670:
                self.playerX = 670
            # Call Player
            self.player(self.playerX, self.playerY)

            # Bullet
            if self.SPACE_KEY:
                if self.bulletState == 'ready':
                    bulletSound = mixer.Sound('sounds/ka-pew.wav')
                    bulletSound.play()
                    self.bulletX = self.playerX
                    self.fireBullet(self.bulletX, self.bulletY)
            if self.bulletY <= 0:
                self.bulletY = 480
                self.bulletState = 'ready'
            if self.bulletState == 'fire':
                self.fireBullet(self.bulletX, self.bulletY)
                self.bulletY -= self.bulletY_change

            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.resetKeys()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curMenu.runDisplay = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.L_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.R_KEY = True
                if event.key == pygame.K_SPACE:
                    self.SPACE_KEY = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.L_KEY = False
                if event.key == pygame.K_RIGHT:
                    self.R_KEY = False

    def resetKeys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.SPACE_KEY = False, False, False, False, False

    def drawText(self, text, size, x, y):
        font = pygame.font.Font(self.fontName, size)
        textSurface = font.render(text, True, self.WHITE)
        textRect = textSurface.get_rect()
        textRect.center = (x, y)
        self.display.blit(textSurface, textRect)

    def showScore(self):
        self.drawText('SCORE: ' + str(self.score), 10, 10, 10)

    def gameOver(self):
        self.drawText('GAME OVER!', 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2)

    def player(self, x, y):
        self.display.blit(self.playerIcon, (x, y))

    def enemy(self, x, y, k):
        self.display.blit(self.enemyIcon[k], (x, y))

    def fireBullet(self, x, y):
        self.bulletState = "fire"
        self.display.blit(self.bulletIcon, (x + 16, y + 10))

    def isColision(self, eneX, eneY, bullX, bullY):
        # Formula for the calculation of the distance of two points
        distance = math.sqrt((math.pow(eneX - bullX, 2)) + (math.pow(eneY - bullY, 2)))
        if distance < 27:
            return True
        else:
            return False
