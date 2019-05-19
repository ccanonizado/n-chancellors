import pygame as pg


# import pages
from pages.menu import Menu
from pages.play import Play

from settings import *

class Game:
    def __init__(self):
        # init pygame
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(TITLE)
    
        self.screen = pg.display.set_mode(BG_SIZE)
        self.running = True
        self.status = MENU

        
    def run(self):
        # Switch page screens
        if self.status == MENU:
            Menu(self)
        elif self.status == PLAY:
            Play(self)


        self.events()
        pg.display.flip()

    def events(self):
        try:
            keys = pg.key.get_pressed()

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