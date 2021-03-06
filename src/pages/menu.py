import sys
import pygame as pg

# move up one directory to be able to import the settings and images
sys.path.append("..")
from ui.Button import Button
from settings import *
from images import *

class Menu:
    def __init__(self, game):
        self.game = game
        self.bg = MENU_BG.convert()

        guide = Button('guide', 120, 590, 267, 78)
        play = Button('play', 475, 550, 267, 78)
        about = Button('about', 815, 590, 267, 78)

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
                    if play.isOver(pos):
                        self.game.status = PLAY
                    elif guide.isOver(pos):
                        self.game.status = GUIDE
                    elif about.isOver(pos):
                        self.game.status = ABOUT

                # mouse hover
                if event.type == pg.MOUSEMOTION:
                    play.isOver(pos)
                    guide.isOver(pos)
                    about.isOver(pos)

            # place loaded elements
            self.game.screen.blit(play.image, (play.x, play.y))
            self.game.screen.blit(guide.image, (guide.x, guide.y))
            self.game.screen.blit(about.image, (about.x, about.y))

            pg.display.flip()