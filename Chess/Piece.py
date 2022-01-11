# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Responsible for pieces.
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import numpy as np
import pygame


def square_can_be_attacked_by_colour(board, colour, square):
    # Colour should be handed to the function in boolean form.
    i = 0
    while (i < 8):
        j = 0
        while (j < 8):
            try:
                if board[j][i].is_white() == colour:
                    match board[j][i].name:
                        case "K":
                            if (abs(i - square[0]) < 2) & (abs(j - square[1]) < 2):
                                return True
                        case "Q":
                            if (valid_diagonal_move(board, (i, j), square) == True) | (valid_horver_move(board, (i, j), square) == True):
                                return True
                        case "R":
                            if (valid_horver_move(board, (i, j), square) == True):
                                return True
                        case "B":
                            if (valid_diagonal_move(board, (i, j), square) == True):
                                return True
                        case "N":
                            if (valid_knight_move(board, (i, j), square) == True):
                                return True
                        case "P":
                            if colour:
                                plus = -1
                            else:
                                plus = 1
                            if (abs(i - square[0]) == 1) & (j + plus == square[1]):
                                return True
                j += 1
            except:
                j += 1
                continue
        i += 1
    return False


def valid_diagonal_move(board, start, end):
    # Firstly see if it goes in the diagonal direction
    if abs(start[0] - end[0]) == abs(start[1] - end[1]):
        if abs(start[0] - end[0]) > 1:
            for i in range(1, abs(start[0] - end[0])):
                if board[start[1] + (np.sign(end[1] - start[1])*i)][start[0] + (np.sign(end[0] - start[0])*i)] != None:
                    return False
        if board[end[1]][end[0]] != None:
            if board[end[1]][end[0]].is_white() == board[start[1]][start[0]].is_white():
                return False
            else:
                return True
        else:
            return True
    else:
        return False


def valid_horver_move(board, start, end):
    # Firstly see if it does move in a horizontal or vertical way
    if (start[0] == end[0]) | (start[1] == end[1]):
        # Checking if there are any pieces in the way
        if max(abs(start[0] - end[0]), abs(start[1] - end[1])) > 1:
            for i in range(1, max(abs(start[0] - end[0]), abs(start[1] - end[1]))):
                if board[start[1] + np.sign(end[1] - start[1])*i][start[0] + np.sign(end[0] - start[0])*i] != None:
                    return False
        # Checking if there is a friendly piece on the end square
        if board[end[1]][end[0]] == None:  # End square is free
            return True
        # Can capture enemy piece
        elif board[end[1]][end[0]].is_white() != board[start[1]][start[0]].is_white():
            return True
        else:
            return False  # Else there is a friendly piece which we cannot move to
    else:
        return False


def valid_knight_move(board, start, end):
    # Easy since knight can jump over stuff. Check it has done an L shape, then check if the square is free/capturable
    if ((abs(start[0] - end[0]) == 2) & (abs(start[1] - end[1]) == 1)) | ((abs(start[0] - end[0]) == 1) & (abs(start[1] - end[1]) == 2)):
        if board[end[1]][end[0]] == None:
            return True
        elif board[end[1]][end[0]].is_white() != board[start[1]][start[0]].is_white():
            return True
        else:
            return False
    else:
        return False


class Piece():
    def __init__(self, colour, image=""):
        self.colour = colour
        self.image = image

    def is_valid_move(self):
        return True

    def is_white(self):
        if self.colour == 'w':
            return True
        else:
            return False

    def __str__(self):
        if self.colour == 'w':
            return self.name
        else:
            return '\033[94m' + self.name + '\033[0m'
            # return self.name.lower()

# We can write functions to check if start and end are on the same row/col/diagonal seperately, and then use them on each of the functions.
# Checking if there is a possible knight move is the other option. This will be put next to the functions mentioned above since this
# will make it clear where all of the code should belong.


class King(Piece):
    def __init__(self, colour, has_moved=False):
        super().__init__(colour)
        self.value = 999
        self.name = "K"
        self.has_moved = has_moved
        if self.is_white() == True:
            self.image = "Chess/Piece_Images/WK.png"
        else:
            self.image = "Chess/Piece_Images/BK.png"

    def can_castle(self, board, start, end):
        if self.has_moved == False:
            match end[0]:
                case 2:
                    try:
                        if (board[start[1]][0].has_moved == False) & (board[start[1]][1] == None) & (board[start[1]][2] == None) & (board[start[1]][3] == None):
                            # Find out if the king is moving through check. No need to check the final square since this is
                            # dealt with by the temp_board
                            if ((square_can_be_attacked_by_colour(board, not self.is_white(), (4, start[1])) == False)
                                & (square_can_be_attacked_by_colour(board, not self.is_white(), (3, start[1])) == False)
                                & (square_can_be_attacked_by_colour(board, not self.is_white(), (2, start[1])) == False)
                                    & (square_can_be_attacked_by_colour(board, not self.is_white(), (4, start[1])) == False)):
                                return True
                            else:
                                return False
                    except:
                        return False
                case 6:
                    try:
                        if (board[start[1]][7].has_moved == False) & (board[start[1]][6] == None) & (board[start[1]][5] == None):
                            if (square_can_be_attacked_by_colour(board, not self.is_white(), (5, start[1])) == False) & (square_can_be_attacked_by_colour(board, not self.is_white(), (6, start[1])) == False) & (square_can_be_attacked_by_colour(board, not self.is_white(), (4, start[1])) == False):
                                return True
                            else:
                                return False
                    except:
                        return False

    def is_valid_move(self, board, ghost_board, start, end):
        if start == end:
            return False  # Preventing moving to own square

        if board[end[1]][end[0]] == None:
            if square_can_be_attacked_by_colour(board, not self.is_white(), end):
                return False
        # Check if trying to castle first. Special case!
        if (self.has_moved == False) & (end[1] == start[1]) & (abs(start[0] - end[0]) == 2):
            return self.can_castle(board, start, end)

        # Check it is moving in the squares around the king, and only taking enemy pieces, and not being allowed on white pieces
        if (start[0] + 1 >= end[0]) & (start[0] - 1 <= end[0]) & (start[1] + 1 >= end[1]) & (start[1] - 1 <= end[1]):
            if board[end[1]][end[0]] != None:
                # Only take opposite colour.
                if board[end[1]][end[0]].is_white() != self.is_white():
                    return True
                else:
                    return False
            return True
        else:
            return False

    def is_in_check(self, board):
        def find_myself(board):  # Woke
            i = 0
            while (i < 8):
                j = 0
                while (j < 8):
                    if board[j][i] != None:
                        if (board[j][i].name == "K") & (board[j][i].is_white() == self.is_white()):
                            return (i, j)
                    j += 1
                i += 1
        kingpos = find_myself(board)
        return square_can_be_attacked_by_colour(board, not self.is_white(), kingpos)


class Queen(Piece):
    def __init__(self, colour, has_moved=False):
        super().__init__(colour)
        self.value = 9
        self.name = "Q"
        if self.is_white() == True:
            self.image = "Chess/Piece_Images/WQ.png"
        else:
            self.image = "Chess/Piece_Images/BQ.png"

    def is_valid_move(self, board, ghost_board, start, end):
        if start == end:
            return False  # Preventing moving to own square

        return (valid_diagonal_move(board, start, end) | valid_horver_move(board, start, end))


class Rook(Piece):
    def __init__(self, colour, has_moved=False):
        self.value = 5
        super().__init__(colour)
        self.name = "R"
        self.has_moved = has_moved
        if self.is_white() == True:
            self.image = "Chess/Piece_Images/WR.png"
        else:
            self.image = "Chess/Piece_Images/BR.png"

    def is_valid_move(self, board, ghost_board, start, end):
        if start == end:
            return False  # Preventing moving to own square

        return valid_horver_move(board, start, end)


class Bishop(Piece):
    def __init__(self, colour, has_moved=False):
        self.value = 3
        super().__init__(colour)
        self.name = "B"
        if self.is_white() == True:
            self.image = "Chess/Piece_Images/WB.png"
        else:
            self.image = "Chess/Piece_Images/BB.png"

    def is_valid_move(self, board, ghost_board, start, end):
        if start == end:
            return False  # Preventing moving to own square

        return valid_diagonal_move(board, start, end)


class Knight(Piece):
    def __init__(self, colour, has_moved=False):
        self.value = 3
        super().__init__(colour)
        self.name = "N"
        if self.is_white() == True:
            self.image = "Chess/Piece_Images/WN.png"
        else:
            self.image = "Chess/Piece_Images/BN.png"

    def is_valid_move(self, board, ghost_board, start, end):
        if start == end:
            return False  # Preventing moving to own square

        return valid_knight_move(board, start, end)


class Pawn(Piece):
    def __init__(self, colour, has_moved=False):
        self.value = 1
        super().__init__(colour)
        self.name = "P"
        self.has_moved = has_moved
        if self.is_white() == True:
            self.image = "Chess/Piece_Images/WP.png"
        else:
            self.image = "Chess/Piece_Images/BP.png"

    def is_valid_move(self, board, ghost_board, start, end):
        if start == end:
            return False  # Preventing moving to own square
        if self.is_white():
            plus = - 1
        else:
            plus = 1
        # Can the pawn move forward one square.
        try:
            if (end[0] == start[0]) & (end[1] == start[1] + plus) & (board[end[1]][end[0]] == None):
                return True
            # Can the pawn move forward two squares.
            elif (end[0] == start[0]) & (end[1] == start[1] + 2*plus) & (board[end[1]][end[0]] == None) & (board[end[1] - plus][end[0]] == None) & (self.has_moved == False):
                return True
            elif (abs(end[0] - start[0]) == 1) & (end[1] == start[1] + plus) & (board[end[1]][end[0]] != None):
                if board[end[1]][end[0]].is_white() != self.is_white():
                    return True
                else:
                    return False
            # The en passent clause
            elif (abs(end[0] - start[0]) == 1) & (end[1] == start[1] + plus) & (board[end[1]][end[0]] == None) & (ghost_board[end[1]][end[0]] != None):
                return True
            else:
                return False
        except:
            return False


class GhostPawn(Piece):
    def __init__(self, colour, has_moved=False):
        self.value = 0
        super().__init__(colour)
        self.name = " "

    def is_valid_move():
        return False
