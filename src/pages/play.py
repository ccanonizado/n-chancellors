import sys
import pygame as pg

# move up one directory to be able to import the settings and images
sys.path.append("..")
from ui.Button import Button
from settings import *
from images import *

class Play:
    def __init__(self, game):
        self.game = game

        home = Button('home', 50, 45, 300, 100)
        fileread = Button('readfile', 50, 190, 300, 100)
        solve = Button('solve', 50, 330, 300, 100)
        next_btn = Button('next', 330, 480, 300, 100)
        back_btn = Button('back', 50, 480, 300, 100)

        while self.game.status == PLAY:
            self.game.screen.blit(PLAY_BG, ORIGIN)

            for event in pg.event.get():
                pos = pg.mouse.get_pos()

                if event.type == pg.QUIT:
                    print("You quit the game!")
                    self.game.running = False
                    quit()
                
                # # mouse click
            #     if event.type == pg.MOUSEBUTTONDOWN:
            #         if play.isOver(pos):
            #             self.game.status = PLAY
            #         elif guide.isOver(pos):
            #             self.game.status = GUIDE
            #         elif about.isOver(pos):
            #             self.game.status = ABOUT

                # mouse hover
                if event.type == pg.MOUSEMOTION:
                    home.isOver(pos)
                    solve.isOver(pos)
                    fileread.isOver(pos)
                    next_btn.isOver(pos)
                    back_btn.isOver(pos)

            self.game.screen.blit(home.image, (home.x, home.y))
            self.game.screen.blit(solve.image, (solve.x, solve.y))
            self.game.screen.blit(fileread.image, (fileread.x, fileread.y))
            self.game.screen.blit(next_btn.image, (next_btn.x, next_btn.y))
            self.game.screen.blit(back_btn.image, (back_btn.x, back_btn.y))

            pg.display.flip()