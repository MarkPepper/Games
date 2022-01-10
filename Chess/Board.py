# %%
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Responsible for GUI and entertaining the user!
# To start, this will simply be a command line.
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import pygame
import Piece
import copy
from typing import Sized
import math
import MoveFinder

screen = pygame.display.set_mode([800, 800])
background_colour = (44, 44, 84)
highlight_colour = pygame.Color(200, 0, 0, 100)


class Square():
    def __init__(self, x_pos, y_pos, size=100, colour=background_colour):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.colour = background_colour
        self.size = size

    def square_drawer(self):
        pygame.draw.rect(screen, self.colour, pygame.Rect(
            self.x_pos, self.y_pos, self.size, self.size))


class Board():
    def __init__(self):
        self.rectangles = []
        self.piece_captured = False
        for i in range(0, 8):
            for j in range(0, 8, 2):
                if i % 2 == 1:
                    self.rectangles.append(Square(i*100, j*100))
                if i % 2 == 0:
                    self.rectangles.append(Square(i*100, (j+1)*100))

        self.pawn_moved = False
        self.white_to_move = True
        self.board = [[None for i in range(0, 8)] for j in range(0, 8)]
        self.ghost_board = [[None for i in range(0, 8)] for j in range(0, 8)]
        self.temp_board = [[None for i in range(0, 8)] for j in range(0, 8)]

        # Setting up the white pieces
        self.board[7][0] = Piece.Rook('w')
        self.board[7][1] = Piece.Knight('w')
        self.board[7][2] = Piece.Bishop('w')
        self.board[7][3] = Piece.Queen('w')
        self.board[7][4] = Piece.King('w')
        self.board[7][5] = Piece.Bishop('w')
        self.board[7][6] = Piece.Knight('w')
        self.board[7][7] = Piece.Rook('w')
        for i in range(0, 8):
            self.board[6][i] = Piece.Pawn('w')

        # Setting up the black pieces
        self.board[0][0] = Piece.Rook('b')
        self.board[0][1] = Piece.Knight('b')
        self.board[0][2] = Piece.Bishop('b')
        self.board[0][3] = Piece.Queen('b')
        self.board[0][4] = Piece.King('b')
        self.board[0][5] = Piece.Bishop('b')
        self.board[0][6] = Piece.Knight('b')
        self.board[0][7] = Piece.Rook('b')
        for i in range(0, 8):
            self.board[1][i] = Piece.Pawn('b')

    def update_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # Creating the background.
        running = True
        # Quit case
        screen.fill((225, 218, 189))
        for rectangle in self.rectangles:
            rectangle.square_drawer()

    def get_player_move(self):
        move = [None, None]
        possible_moves = []
        clock = pygame.time.Clock()
        while (True):
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        quit()
                    
                    case pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        square = (int(math.floor(mouse_pos[0]/100)), int(math.floor(mouse_pos[1]/100)))
                        if (move[0] == None):
                            if (self.board[square[1]][square[0]] == None):
                                move = [None, None]
                                possible_moves = []
                                self.print_board()
                                continue
                            elif (self.board[square[1]][square[0]].is_white() != self.white_to_move):
                                move = [None, None]
                                possible_moves = []
                                self.print_board()
                                continue
                            else:
                                possible_moves = MoveFinder.piece_move_finder(self, square)
                                move = [square, None]
                                self.print_board(possible_moves + [(move[0][0], move[0][1])])
                                continue
                        else:
                            if square in possible_moves:
                                move[1] = square
                                return move
                            else:
                                move = [None, None]
                                possible_moves = []
                                self.print_board()
                                continue

            clock.tick(60)

    def piece_loader(self, xpos, ypos, image):
        chess_image = pygame.image.load(image)
        screen.blit(chess_image, (xpos, ypos))

    def print_board(self, highlights = []):
        self.update_screen()
        for i in range(0, 8):
            for j in range(0, 8):
                if (i,j) in highlights:
                    rect = pygame.Surface((100, 100), pygame.SRCALPHA)
                    rect.fill(highlight_colour)
                    screen.blit(rect, (i*100, j*100))
                if self.board[i][j] == None:
                    continue
                else:
                    self.piece_loader(j*100, i*100, self.board[i][j].image)

        pygame.display.update()

    def valid_move(self, board, start, end):
        # Ensures that a piece has been chosen.
        # Ensures that a null move (i.e. moving a piece to where it currently is) is not allowed.
        if board[start[1]][start[0]] == None or start == end:
            return False
        elif self.white_to_move != board[start[1]][start[0]].is_white():
            return False
        else:
            return board[start[1]][start[0]].is_valid_move(board, self.ghost_board, start, end)
            # Currently just finds if it is a valid move, and then performs the move. It should perform the move on the temp board, check
            # if they have not discovered themselves, and then only then can they determine if the move is valid or not.

    def temp_valid_move(self, moving_colour, start, end):
        # Ensures that a piece has been chosen.
        # Ensures that a null move (i.e. moving a piece to where it currently is) is not allowed.
        if self.temp_board[start[1]][start[0]] == None or start == end:
            return False
        elif moving_colour != self.temp_board[start[1]][start[0]].is_white():
            return False
        else:
            return self.temp_board[start[1]][start[0]].is_valid_move(self.temp_board, self.ghost_board, start, end)

    def move(self, start, end):
        def en_passent_logic(start, end):
            # Updating ghost board for en passent reasons.
            self.ghost_board = [
                [None for i in range(0, 8)] for j in range(0, 8)]
            if (self.board[start[1]][start[0]].name == "P") & (abs(start[1] - end[1]) == 2):
                self.ghost_board[int((start[1] + end[1])/2)][start[0]
                                                             ] = Piece.GhostPawn(self.board[start[1]][start[0]].colour)

            # Some extra logic to remove the enemy pawn if we are doing en passent.
            if (self.board[start[1]][start[0]].name == "P") & (start[0] != end[0]) & (self.board[end[1]][end[0]] == None):
                self.board[end[1] + 1][end[0]] = None
                # Fine to set both to none, since if ghost pawn is present, then opposite pawn has only just
                self.board[end[1] - 1][end[0]] = None
                # moved, and thus both the squares above and below where were are moving to are where the pawn was and where the pawn is... i.e. we
                # want to remove where the pawn is, and where the pawn was is empty anyway.

        def check_pawn_promotion(start, end):
            # PAWN PROMOTION Logic
            if (self.board[start[1]][start[0]].name == "P") & ((end[1] == 7) | (end[1] == 0)):
                promoted = False
                while (not promoted):
                    promote_to = input(
                        "What would you like to promote to? (Enter 'Q' for Queen, etc.) ")
                    match promote_to:
                        case "Q":
                            self.board[end[1]][end[0]] = Piece.Queen(
                                self.board[start[1]][start[0]].colour, True)
                            promoted = True
                        case "R":
                            self.board[end[1]][end[0]] = Piece.Rook(
                                self.board[start[1]][start[0]].colour, True)
                            promoted = True
                        case "B":
                            self.board[end[1]][end[0]] = Piece.Bishop(
                                self.board[start[1]][start[0]].colour, True)
                            promoted = True
                        case "N":
                            self.board[end[1]][end[0]] = Piece.Knight(
                                self.board[start[1]][start[0]].colour, True)
                            promoted = True
        if self.board[start[1]][start[0]].name == "P":
            self.pawn_moved = True
        else:
            self.pawn_moved = False

        if self.board[end[1]][end[0]] != None:
            self.piece_captured = True
        else:
            self.piece_captured = False

        castling = False
        if self.board[start[1]][start[0]].name == "K":
            if (end[1] == start[1]) & (abs(start[0] - end[0]) == 2):
                castling = True
                match end[0]:
                    case 2:
                        self.board[start[1]][start[0]].has_moved = True
                        self.board[end[1]][end[0]
                                           ] = self.board[start[1]][start[0]]
                        self.board[start[1]][start[0]] = None
                        self.board[start[1]][end[0] +
                                             1] = self.board[start[1]][0]
                        self.board[start[1]][0] = None
                    case 6:
                        self.board[start[1]][start[0]].has_moved = True
                        self.board[end[1]][end[0]
                                           ] = self.board[start[1]][start[0]]
                        self.board[start[1]][start[0]] = None
                        self.board[start[1]][end[0] -
                                             1] = self.board[start[1]][7]
                        self.board[start[1]][7] = None

        if (not castling):
            en_passent_logic(start, end)
            self.board[start[1]][start[0]].has_moved = True
            self.board[end[1]][end[0]] = self.board[start[1]][start[0]]
            check_pawn_promotion(start, end)
            self.board[start[1]][start[0]] = None

    def temp_move(self, start, end):
        def en_passent_logic(start, end):
            # Some extra logic to remove the enemy pawn if we are doing en passent.
            if (self.temp_board[start[1]][start[0]].name == "P") & (start[0] != end[0]) & (self.temp_board[end[1]][end[0]] == None):
                self.temp_board[end[1] + 1][end[0]] = None
                # Fine to set both to none, since if ghost pawn is present, then opposite pawn has only just
                self.temp_board[end[1] - 1][end[0]] = None
                # moved, and thus both the squares above and below where were are moving to are where the pawn was and where the pawn is... i.e. we
                # want to remove where the pawn is, and where the pawn was is empty anyway.

        def check_pawn_promotion(start, end):
            # PAWN PROMOTION Logic
            if (self.temp_board[start[1]][start[0]].name == "P") & ((end[1] == 7) | (end[1] == 0)):
                self.temp_board[end[1]][end[0]] = Piece.Queen(
                    self.temp_board[start[1]][start[0]].colour, True)

        castling = False
        if self.temp_board[start[1]][start[0]].name == "K":
            if (end[1] == start[1]) & (abs(start[0] - end[0]) == 2):
                castling = True
                match end[0]:
                    case 2:
                        self.temp_board[start[1]][start[0]].has_moved = True
                        self.temp_board[end[1]][end[0]
                                                ] = self.temp_board[start[1]][start[0]]
                        self.temp_board[start[1]][start[0]] = None
                        self.temp_board[start[1]][end[0] +
                                                  1] = self.temp_board[start[1]][0]
                        self.temp_board[start[1]][0] = None
                    case 6:
                        self.temp_board[start[1]][start[0]].has_moved = True
                        self.temp_board[end[1]][end[0]
                                                ] = self.temp_board[start[1]][start[0]]
                        self.temp_board[start[1]][start[0]] = None
                        self.temp_board[start[1]][end[0] -
                                                  1] = self.temp_board[start[1]][7]
                        self.temp_board[start[1]][7] = None
        if (not castling):
            # Standard procedure otherwise.
            en_passent_logic(start, end)
            self.temp_board[start[1]][start[0]].has_moved = True
            self.temp_board[end[1]][end[0]
                                    ] = self.temp_board[start[1]][start[0]]
            check_pawn_promotion(start, end)
            self.temp_board[start[1]][start[0]] = None

    # def check_in_check(self):
    #     #Will be used on temp check. Will find if they have put themselves in check after a move.
    #     def find_king():
    #         i = 0
    #         while (i < 8):
    #             j = 0
    #             while (j < 8):
    #                 if self.temp_board[j][i] != None:
    #                     if (self.temp_board[j][i].name == "K") & (self.temp_board[j][i].is_white() == self.white_to_move):
    #                         return (i,j)
    #                 j += 1
    #             i += 1
    #     king_pos = find_king()
    #     for i in range(0,8):
    #         for j in range(0,8):
    #             if self.temp_board[j][i] != None:
    #                 if self.temp_board[j][i].is_white() != self.white_to_move:
    #                     return self.temp_valid_move(not self.white_to_move, (i,j), king_pos)
    #     return False

    def check_self_discovery(self, start, end):
        # See if a move has put themselves in check. E.g. moving a pinned piece (or the weird lateral discovery after en passent)
        self.temp_board = copy.deepcopy(self.board)
        self.temp_move(start, end)
        kingpos = self.find_king(self.temp_board)
        return self.temp_board[kingpos[1]][kingpos[0]].is_in_check(self.temp_board)

    def find_king(self, board):  # Woke
        i = 0
        while (i < 8):
            j = 0
            while (j < 8):
                if board[j][i] != None:
                    if (board[j][i].name == "K") & (board[j][i].is_white() == self.white_to_move):
                        return (i, j)
                j += 1
            i += 1

    # Returns false if moving the selected piece causes the king to no longer be in check
    def attempt_all_moves(self, start):
        self.temp_board = copy.deepcopy(self.board)
        i = 0
        while (i < 8):
            j = 0
            while (j < 8):
                if self.temp_valid_move(self.white_to_move, start, (i, j)) == True:
                    self.temp_move(start, (i, j))
                    kingpos = self.find_king(self.temp_board)
                    if (not self.temp_board[kingpos[1]][kingpos[0]].is_in_check(self.temp_board)):
                        return False
                    self.temp_board = copy.deepcopy(self.board)
                j += 1
            i += 1
        return True

    def check_for_mate(self):
        # The self.colour is the colour of the team that might be in checkmate.

        # Firstly check that they are in check.
        kingpos = self.find_king(self.board)
        if (not self.board[kingpos[1]][kingpos[0]].is_in_check(self.board)):
            return False
        # If the king is not in check, mate is false. If the king IS in check, we continuewith the logic below.

        i = 0
        while (i < 8):
            j = 0
            while (j < 8):
                try:
                    if (self.board[j][i].is_white() == self.white_to_move):
                        if (not self.attempt_all_moves((i, j))):
                            return False
                    j += 1
                except:
                    j += 1
            i += 1

        return True

    def check_for_stalemate(self):
        # This is actually the same as checkmate, but for the fact that the player is not currently in check.
        kingpos = self.find_king(self.board)
        if (self.board[kingpos[1]][kingpos[0]].is_in_check(self.board)):
            return False

        i = 0
        while (i < 8):
            j = 0
            while (j < 8):
                try:
                    if (self.board[j][i].is_white() == self.white_to_move):
                        if (not self.attempt_all_moves((i, j))):
                            return False
                    j += 1
                except:
                    j += 1
            i += 1

        return True

    def reset_halfmove_clock(self):
        return (self.piece_captured | self.pawn_moved)


# %%
