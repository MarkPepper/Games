import numpy as np

class Grid:
    def __init__(self,initial_board):
        self.grid = initial_board

    def check_legal_grid(self, grid):
        #checking columns
        
        for i in range(0,8):
            values_in_col = []
            for j in range(0,8):
                if (grid[j][i] != None):
                    if grid[j][i] in values_in_col:
                        return False
                    else:
                        values_in_col.append(grid[j][i])

        #Checking rows
        for i in grid:
            values_in_row = []
            for j in i:
                if (j != None):
                    if j in values_in_row:
                        return False
                    else:
                        values_in_row.append(j)

        grid = np.array(grid)
        for i in range(0,3):
            for j in range(0,3):
                subgrid = grid[i*3:i*3 + 3, j*3: j*3 + 3]
                subgrid = subgrid.reshape(9)
                values_in_subgrid = []
                for k in subgrid:
                    if (k != None):
                        if k in values_in_subgrid:
                            return False
                        else:
                            values_in_subgrid.append(k)

        return True