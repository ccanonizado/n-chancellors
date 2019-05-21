'''
This is the main game file!

All the other classes are distributed in the different directories:
- /src/ui - Button.py, Tile.py
- /src/pages/ - menu.py, play.py, solution.py 

Other classes used in this directory are:
- settings.py for all the configurations needed
- images.py for all the photos imported

'''

import pygame as pg

# import pages
from pages.menu import Menu
from pages.play import Play
from pages.solution import Solution

from settings import *

class Game:
    def __init__(self):
        # init pygame
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(TITLE)
    
        self.screen = pg.display.set_mode(BG_SIZE)
        self.init = False # Check if game has started
        self.running = True
        self.status = MENU

        
    def run(self):
        # Switch page screens
        if self.status == MENU:
            Menu(self)
        elif self.status == PLAY:
            Play(self)
        elif self.status == SOLUTION:
            Solution(self)

        self.events()
        pg.display.flip()

    def events(self):
        try:
            # Get all events
            for event in pg.event.get():
                # check for closing window
                if event.type == pg.QUIT:                    
                    print("You quit the game!")
                    self.running = False
                    quit()
        except:
            quit()


game = Game()

while game.running:
    game.run()