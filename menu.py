import pygame


class Menu:
    def __init__(self, game):
        self.game = game
        self.midW, self.midH = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.runDisplay = True
        self.cursorRect = pygame.Rect(0, 0, 20, 20)
        self.offset = -150

    def drawCursor(self):
        self.game.drawText("*", 15, self.cursorRect.x, self.cursorRect.y)

    def blitScreen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.resetKeys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.midW, self.midH
        self.optionsx, self.optionsy = self.midW, self.midH + 50
        self.creditsx, self.creditsy = self.midW, self.midH + 100
        self.cursorRect.midtop = (self.startx + self.offset, self.starty)

    def displayMenu(self):
        self.runDisplay = True
        while self.runDisplay:
            self.game.checkEvents()
            self.checkInput()
            self.game.display.fill(self.game.BLACK)
            self.game.drawText("MAIN MENU", 30, self.game.DISPLAY_W / 2, 50)
            self.game.drawText("START GAME", 20, self.startx, self.starty)
            self.game.drawText("OPTIONS", 20, self.optionsx, self.optionsy)
            self.game.drawText("CREDITS", 20, self.creditsx, self.creditsy)
            self.drawCursor()
            self.blitScreen()

    def moveCursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursorRect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursorRect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursorRect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
        if self.game.UP_KEY:
            if self.state == "Start":
                self.cursorRect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Options":
                self.cursorRect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
            elif self.state == "Credits":
                self.cursorRect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"

    def checkInput(self):
        self.moveCursor()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.playing = True
            elif self.state == "Options":
                self.game.curMenu = self.game.options
            elif self.state == "Credits":
                self.game.curMenu = self.game.credits
            self.runDisplay = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.midW, self.midH
        self.controlsx, self.controlsy = self.midW, self.midH + 50
        self.cursorRect.midtop = (self.volx + self.offset, self.voly)

    def displayMenu(self):
        self.runDisplay = True
        while self.runDisplay:
            self.game.checkEvents()
            self.checkInput()
            self.game.display.fill((0, 0, 0))
            self.game.drawText('OPTIONS', 30, self.game.DISPLAY_W / 2, 50)
            self.game.drawText('VOLUME', 20, self.volx, self.voly)
            self.game.drawText('CONTROLS', 20, self.controlsx, self.controlsy)
            self.drawCursor()
            self.blitScreen()

    def checkInput(self):
        if self.game.BACK_KEY:
            self.game.curMenu = self.game.mainMenu
            self.runDisplay = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursorRect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursorRect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            # to-do: create Volume and Controls menu
            pass


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def displayMenu(self):
        self.runDisplay = True
        while self.runDisplay:
            self.game.checkEvents()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curMenu = self.game.mainMenu
                self.runDisplay = False
            self.game.display.fill(self.game.BLACK)
            self.game.drawText('CREDITS', 30, self.game.DISPLAY_W / 2, 50)
            self.game.drawText('MADE BY SUSANNE KOLJONEN', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
            self.blitScreen()
