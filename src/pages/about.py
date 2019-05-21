import sys
import pygame as pg

# move up one directory to be able to import the settings and images
sys.path.append("..")
from ui.Button import Button
from settings import *
from images import *

class About:
    def __init__(self, game):
        self.game = game
        self.bg = ABOUT_BG.convert()

        home = Button('home', 50, 45, 63, 63)

        while self.game.status == MENU:
            self.game.screen.blit(self.bg, ORIGIN)

            for event in pg.event.get():
                pos = pg.mouse.get_pos()

                if event.type == pg.QUIT:
                    print("You quit the game!")
                    self.game.running = False
                    quit()
                
                # mouse click
                if event.type == pg.MOUSEBUTTONDOWN:
                    # change screens on mouse click
                    if home.isOver(pos):
                        self.game.status = MENU

                # mouse hover
                if event.type == pg.MOUSEMOTION:
                    home.isOver(pos)

            # place loaded elements
            self.game.screen.blit(home.image, (home.x, home.y))

            pg.display.flip()