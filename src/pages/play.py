import sys
import pygame as pg

# move up one directory to be able to import the settings and images
sys.path.append("..")
from ui.Button import Button
from ui.Tile import  Tile
from settings import *
from images import *

class Play:
    def __init__(self, game):
        self.game = game
        self.bg = PLAY_BG.convert()

        # if game has not started, initialize variables
        if (self.game.init == 0):
            self.game.current_board = 0  # Current board being diplayed
            self.game.boards = []
            self.game.board_lengths = [] # Array containing sizes of the boards 
            self.game.board_images = [] # Array of images to be displayed
            self.game.init = 1

        home = Button('home', 50, 45, 63, 63)
        fileread = Button('readfile', 50, 190, 315, 61)
        addboard = Button('addboard', 50, 300, 315, 61)
        solve = Button('solve', 50, 435, 217, 61)
        back_btn = Button('back', 50, 570, 55, 55)
        next_btn = Button('next', 380, 570, 55, 55)

        while self.game.status == PLAY:
            self.game.screen.blit(self.bg, ORIGIN)

            # get all events
            for event in pg.event.get():
                # Get mouse position
                pos = pg.mouse.get_pos()

                # Player presses exit
                if event.type == pg.QUIT:
                    print("You quit the game!")
                    self.game.running = False
                    quit()
                
                # mouse click
                if event.type == pg.MOUSEBUTTONDOWN:
                    if home.isOver(pos):
                        self.game.status = MENU
                    elif fileread.isOver(pos):
                        self.getBoardFile()
                    elif solve.isOver(pos):
                        # check if there are input boards
                        if self.game.boards:
                            # go to solution of current board
                            self.game.status = SOLUTION
                            
                    # Display next board
                    elif next_btn.isOver(pos):
                        if self.game.boards: # if input boards are not empty
                            self.game.current_board = (self.game.current_board + 1) % len(self.game.boards)
                            self.displayBoard()
                            
                    # Display previous board
                    elif back_btn.isOver(pos):
                        if self.game.boards: # if input boards are not empty
                            self.game.current_board = (self.game.current_board - 1) % len(self.game.boards)
                            self.displayBoard()

                    # iterate through entire current display
                    # if user clicks on tile, toggle tile chancy image
                    if self.game.board_lengths:
                        for row in range(self.game.board_lengths[self.game.current_board]):
                            for col in range(self.game.board_lengths[self.game.current_board]):
                                if self.game.board_images[row][col].isOver(pos):
                                    if self.game.boards[self.game.current_board][row][col] == '1':
                                        self.game.boards[self.game.current_board][row][col] = '0'
                                    else:
                                        self.game.boards[self.game.current_board][row][col] = '1'
                                    self.displayBoard()


                # mouse hover
                if event.type == pg.MOUSEMOTION:
                    home.isOver(pos)
                    fileread.isOver(pos)
                    addboard.isOver(pos)
                    solve.isOver(pos)
                    back_btn.isOver(pos)
                    next_btn.isOver(pos)

            # Display loaded elements
            self.game.screen.blit(home.image, (home.x, home.y))
            self.game.screen.blit(fileread.image, (fileread.x, fileread.y))
            self.game.screen.blit(addboard.image, (addboard.x, addboard.y))
            self.game.screen.blit(solve.image, (solve.x, solve.y))
            self.game.screen.blit(back_btn.image, (back_btn.x, back_btn.y))
            self.game.screen.blit(next_btn.image, (next_btn.x, next_btn.y))
            self.game.screen.blit(BOARD_LABEL, (152, 575))

            # Display current board number if board not empty
            if self.game.boards:
                pg.font.init()
                myfont = pg.font.SysFont('Big John', 36)
                currentboard = '%d/%d' % (self.game.current_board, len(self.game.boards)-1)
                textsurface = myfont.render(currentboard, True, (1, 1, 1))
                self.game.screen.blit(textsurface,(210,640))

            # Display current board
            if self.game.board_lengths:
                for row in range(self.game.board_lengths[self.game.current_board]):
                    for col in range(self.game.board_lengths[self.game.current_board]):
                        self.game.screen.blit(self.game.board_images[row][col].image, (self.game.board_images[row][col].x, self.game.board_images[row][col].y))

            pg.display.flip()
    # # for testing
    # def printBoards(self):
    #     for x in range(len(self.game.boards)):
    #         board_size = self.game.board_lengths[x]
    #         for row in range(board_size):
    #             for col in range(board_size):
    #                 print(self.game.boards[x][row][col], end=" ")
    #             print("")
    #         print("")

    # This functions gets input boards from a file and adds it to the array of boards
    def getBoardFile(self):
        f = open("input.txt", "r")

        # Get number of inputs from first line of file
        num_inputs = int(f.readline())

        # Get boards based from the number of inputs
        for x in range(num_inputs):
            new_board = [] # Initialize new board
            board_size = int(f.readline()) # Get board size
            self.game.board_lengths.append(board_size)
            for i in range(board_size):
                board_row = f.readline().splitlines()[0].split(" ") # Get row of board
                new_board.append(board_row)
            self.game.boards.append(new_board) # Add new board to list of boards
            new_board = [] # Empty array for new row

        f.close()

        self.displayBoard()
    
    # Display current board
    def displayBoard(self):
        # Empty board_images array
        self.game.board_images = []

        image_row = [] # initialize row of images to be pushed
        
        # x and y position where the board will start generating
        # Depending on the board size, the starting points will be different
        # 3 x 3
        if (self.game.board_lengths[self.game.current_board] == 3):
            start_x = 755
            start_y = 220
        # 4 x 4
        elif (self.game.board_lengths[self.game.current_board] == 4):
            start_x = 720
            start_y = 185
        # 5 x 5
        elif (self.game.board_lengths[self.game.current_board] == 5):
            start_x = 680
            start_y = 150
        # 6 x 6
        elif (self.game.board_lengths[self.game.current_board] == 6):
            start_x = 647
            start_y = 102
        # 7 x 7
        elif (self.game.board_lengths[self.game.current_board] == 7):
            start_x = 612
            start_y = 80
        # 8 x 8
        elif (self.game.board_lengths[self.game.current_board] == 8):
            start_x = 576
            start_y = 30


        # Board size of current board
        board_size = self.game.board_lengths[self.game.current_board]
        
        # will be added for tile spacing
        itr_x = 0
        itr_y = 0

        # Initial tile type
        tile_type = 'white_tile'

        # iterate through current board and append to array of images to display
        for row in range(board_size):
            for col in range(board_size):
                # Check if tile has a chancellor
                if self.game.boards[self.game.current_board][row][col] == '1':
                    image_row.append(Tile(tile_type+'_chancy', True, start_x+itr_x, start_y+itr_y, 70, 71))
                else:
                    image_row.append(Tile(tile_type, False, start_x+itr_x, start_y+itr_y, 70, 71))
                # Change tile color per col
                tile_type = 'blue_tile' if tile_type == 'white_tile' else 'white_tile'
                itr_x += 70 # move x to adjust print
            self.game.board_images.append(image_row)
            itr_x = 0
            itr_y += 71 # move y to adjust print
            image_row = [] #empty array for new row
            # Change tile color per row
            tile_type = 'blue_tile' if tile_type == 'white_tile' else 'white_tile'

        pg.display.update()