import sys
import subprocess
import pygame as pg

# move up one directory to be able to import the settings and images
sys.path.append("..")
from ui.Button import Button
from ui.Tile import  Tile
from settings import *
from images import *

class Solution:
    def __init__(self, game):
        self.game = game
        self.bg = PLAY_BG.convert()
        self.solution_board_size = self.game.board_lengths[self.game.current_board]
        self.solution_boards = [] # initialize 3d array to contain solutions
        self.solution_images = [] # images to contain current solution
        self.current_solution = 0
        self.number_of_solutions = 0
        self.no_solutions = False
        self.input_current_solution = ''
        self.input_box_active = False
        # Create rec where input will be displayed
        self.input_box = pg.Rect(178, 550, 140, 38)

        back_btn2 = Button('back_soln', 50, 45, 63, 63)
        back_btn = Button('back', 55, 330, 55, 55)
        next_btn = Button('next', 440, 330, 55, 55)
        
        # write solution to file to be read by solver
        self.writeSolution()

        # run the sovler to get solutions
        if(self.getSolution()):
            self.displaySolution()

        while self.game.status == SOLUTION:
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
                    if back_btn2.isOver(pos):
                        self.game.status = PLAY
                    # Display next board
                    elif next_btn.isOver(pos):
                        if self.solution_boards: # if input boards are not empty
                            self.current_solution = (self.current_solution + 1) % self.number_of_solutions
                            self.displaySolution()
                    # Display previous board
                    elif back_btn.isOver(pos):
                        if self.solution_boards: # if input boards are not empty
                            self.current_solution = (self.current_solution - 1) % self.number_of_solutions
                            self.displaySolution()
                    
                    # If the user clicked on the input_box rect.
                    if self.input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        self.input_box_active = not self.input_box_active
                    else:
                        self.input_box_active = False
                
                # if input box is used
                elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_RETURN:
                            # Check if inputted solution number is within range
                            if( (int(self.input_current_solution) <= self.number_of_solutions) and (int(self.input_current_solution) > 0)):
                                self.current_solution = int(self.input_current_solution)-1
                                self.displaySolution()
                            self.input_current_solution = ''
                        elif event.key == pg.K_BACKSPACE:
                            self.input_current_solution = self.input_current_solution[:-1]
                        else:
                            self.input_current_solution += event.unicode

                # mouse hover
                if event.type == pg.MOUSEMOTION:
                    back_btn2.isOver(pos)
                    back_btn.isOver(pos)
                    next_btn.isOver(pos)

            # Display current board number if solutions were found
            if self.solution_boards:
                # Display current solution
                pg.font.init()
                font = pg.font.SysFont('Big John', 36)
                currentboard = '%d/%d' % (self.current_solution+1,self.number_of_solutions)
                textsurface = font.render(currentboard, True, (1, 1, 1))
                self.game.screen.blit(textsurface,(230,410))
                
                # Display the user input text field for solution
                txt_surface = font.render(self.input_current_solution, True, pg.Color('black'))
                # Resize the box if the text is too long.
                width = max(200, txt_surface.get_width()+10)
                self.input_box.w = width
                # Blit the text.
                self.game.screen.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))
                # Blit the input_box rect.
                pg.draw.rect(self.game.screen, pg.Color('white'), self.input_box, 2)
            
            # Display loaded elements
            self.game.screen.blit(back_btn2.image, (back_btn2.x, back_btn2.y))
            
            # Display current solution board
            if self.solution_boards:
                for row in range(self.solution_board_size):
                    for col in range(self.solution_board_size):
                        self.game.screen.blit(self.solution_images[row][col].image, (self.solution_images[row][col].x, self.solution_images[row][col].y))
            # Check if solutions were found
            if not self.no_solutions:
                self.game.screen.blit(SOLUTIONS_LABEL, (130, 340))
                self.game.screen.blit(INPUT_SOLN_LABEL, (104, 500))
                self.game.screen.blit(back_btn.image, (back_btn.x, back_btn.y))
                self.game.screen.blit(next_btn.image, (next_btn.x, next_btn.y))
                self.game.screen.blit(SOLUTIONS_HEADER, (625, 40))
            # if no solutions were found, show no solutions label
            else: 
                self.game.screen.blit(NO_SOLUTIONS_LABEL, (143, 320))
            pg.display.flip()

    def writeSolution(self):
        # initialize file for solver to write on
        f = open("solver_input.txt", "w")

        # write number of inputs
        f.write('1\n')

        # write board size
        f.write(str(self.solution_board_size)+'\n')
        
        # iterate through current board and write the board in file
        for row in range(self.solution_board_size):
            for col in range(self.solution_board_size):
                f.write(self.game.boards[self.game.current_board][row][col] + ' ')
            f.write('\n')
        
        f.close()

    def getSolution(self):
        # PARSE OUTPUT OF SOLVER
        #  Run solver on  the current board then parse the output
        command = "solver.exe" # ./solver/solver = MAC | solver.exe = WINDOWS
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0]
        
        # convert result to ascii
        result = result.decode('ascii')

        print()

        # remove \n and \r from the string
        result = result.split('\n')
        for i in range(0, len(result)):
            result[i] = result[i].replace('\r', "")
        
        # check if there is a solution
        if(result[0] == "NO SOLUTION"):
            self.no_solutions = True
            return False

        # Remove empty strings
        result = list(filter(None, result))

        # Get number of solutions (last line of output)
        self.number_of_solutions = int(result[len(result)-1])

        # remove number of solutons from solutions array
        result.remove(result[len(result)-1])
        
        # move through each line by this counter
        counter = 0
        # iterate through results and turn split every string into single letters
        for x in range(self.number_of_solutions):
            new_solution_board = [] # initialize new solution board
            for i in range(self.solution_board_size): # get each row of solution
                new_solution_row = result[counter].split(" ")[:(self.solution_board_size)]
                new_solution_board.append(new_solution_row) # append row to current solution board
                counter += 1
            self.solution_boards.append(new_solution_board) # append board to the solution boards
            new_solution_board = []
        return True
    
    # Display current solution
    def displaySolution(self):
        # Empty board_images array
        self.solution_images = []

        image_row = [] # initialize row of images to be pushed
        
        # x and y position where the board will start generating
        # Depending on the board size, the starting points will be different
        # 3 x 3
        if (self.solution_board_size == 3):
            start_x = 740
            start_y = 268
        # 4 x 4
        elif (self.solution_board_size == 4):
            start_x = 705
            start_y = 230
        # 5 x 5
        elif (self.solution_board_size == 5):
            start_x = 670
            start_y = 195
        # 6 x 6
        elif (self.solution_board_size == 6):
            start_x = 630
            start_y = 150
        # 7 x 7
        elif (self.solution_board_size == 7):
            start_x = 600
            start_y = 125
        # 8 x 8
        elif (self.solution_board_size == 8):
            start_x = 565
            start_y = 80
        
        # will be added for tile spacing
        itr_x = 0
        itr_y = 0

        # Initial tile type
        tile_type = 'white_tile'

        # iterate through current board and append to array of images to display
        for row in range(self.solution_board_size):
            for col in range(self.solution_board_size):
                # Check if tile has a chancellor
                if self.solution_boards[self.current_solution][row][col] == 'C':
                    image_row.append(Tile(tile_type+'_chancy', True, start_x+itr_x, start_y+itr_y, 70, 71))
                else:
                    image_row.append(Tile(tile_type, False, start_x+itr_x, start_y+itr_y, 70, 71))
                # Change tile color per col
                tile_type = 'blue_tile' if tile_type == 'white_tile' else 'white_tile'
                itr_x += 70 # move x to adjust print
            self.solution_images.append(image_row)
            itr_x = 0
            itr_y += 71 # move y to adjust print
            image_row = [] #empty array for new row

            # Change tile color again if board size is even
            if(self.solution_board_size % 2 == 0):
                tile_type = 'blue_tile' if tile_type == 'white_tile' else 'white_tile'

        pg.display.update()