import os
import pygame as pg

# add the path to the folder with the button images
img_path = os.path.abspath(os.curdir) + '/images/game/'

class Tile:
    def __init__(self, tile, isChancy, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.isChancy = isChancy
        self.image = pg.image.load(img_path+tile+'.png')
    # returns True and changes image if mouse is inside button
    # else returns False and retains original image
    def isOver(self, pos):
        # pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True
        return False