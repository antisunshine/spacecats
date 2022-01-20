from game import Game

g = Game()

while g.running:
    g.curMenu.displayMenu()
    g.gameLoop()