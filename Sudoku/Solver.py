#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


class Flora:
    def __init__(self, food, silly_voice):
        self.silly_voice = silly_voice
        self.talent = food

    def __str__(self):
        return ('We thank thy Flora for thy ' + self.talent)

import numpy as np
import pygame
import Sudoku

pygame.init()
screen = pygame.display.set_mode((450,450))
pygame.display.set_caption('Sudoku Solver')

class Solver:
    def __init__(self, initial_board):
        self.grid = Sudoku.Grid(initial_board)
        self.legend = Flora('food', 'German')

    def backtracking_algorithm(self):
        grid = np.array(self.grid.grid) #Here you go Eddie. A horrible overuse of grid as promised. I know how much you love it <3
        grid = grid.reshape(81)
        empties = (grid == None)
        pointer = 0
        backtrack = False
        while pointer < 81:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            if (empties[pointer]) & (backtrack == False):
                #In this section, we check if the cell currently has nothing in (i.e, we then put a 1 in it), or if it is x < 9, we add one.
                #In fact, in the case that we incriment to 9, if the thing still doesn't work, then we need to backtrack.
                if grid[pointer] == None:
                    grid[pointer] = 1
                elif grid[pointer] < 9:
                    grid[pointer] += 1

                if self.grid.check_legal_grid(grid.reshape([9,9])):
                    pointer += 1
                else:
                    if (grid[pointer] >= 9):
                        grid[pointer] = None
                        pointer -= 1
                        backtrack = True

            elif (not empties[pointer]) & (backtrack == True):
                pointer -= 1
            elif (empties[pointer]) & (backtrack == True):
                if (grid[pointer] == 9):
                    grid[pointer] = None
                    pointer -= 1
                else:
                    backtrack = False
            elif (not empties[pointer]) & (backtrack == False):
                pointer += 1


            #print(grid.reshape([9,9]))
            print(self.legend)
        print(grid.reshape([9,9]))


    def print_board(self, grid):
        for i in range(1,8):
            r = pygame.Rect(i*50 - 2, -10, 4, 500)
            pygame.draw.rect(screen, (0,0,0), r)
            r = pygame.Rect(-2, i*50 - 2, 460, 4)
            pygame.draw.rect(screen, (0,0,0), r)

        for i in range(1,3):
            r = pygame.Rect(i*150 - 4, -10, 8, 500)
            pygame.draw.rect(screen, (0,0,0), r)
            r = pygame.Rect(-2, i*150 - 4, 460, 8)
            pygame.draw.rect(screen,(0,0,0), r)
        font = pygame.font.Font('freesansbold.ttf', 12)
        for i in range(0,8):
            for j in range(0,8):
                if (grid[j][i] != None):
                    text = font.render(str(grid[j][i]), True, (0,0,0))
                    textRect = text.get_rect()
                    textRect.center = (i*50 + 25, j*50 + 25)
                    screen.blit(text, textRect)

        pygame.display.update()



def main():

    initial_board = [[None, None, None, None, None, None, 3, None, None],
                    [None, None, None, None, None, None, None, 9, None],
                    [None, None, None, 4,8,3,5, None, 7],
                    [1, None,None, None, None,None,9, None, None],
                    [None,7,9,6,None,None,4,None,None],
                    [8,None,None,9,7,None,2,None,None],
                    [None,6,1,None,5,None,None,None,None],
                    [2,None,3,None,4,None,None,None,None],
                    [None,5,None,8,None,7,None,None,None]]

    
    solver = Solver(initial_board)
    solver.backtracking_algorithm()


if __name__ == "__main__":
    
    main()