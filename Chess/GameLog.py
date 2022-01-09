# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Responsible for keeping a log of the game.
# The positions will be recorded in FEN notation.
# I believe that this will not occupy much space, and give me practice at string manipulation.
# I do not intend to use FEN notation to train an AI!
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

class GameLog():
    def __init__(self):
        self.history = []
        self.halfmove_clock = 0

    def check_for_repetition(self):
        # Make the move on the game first, then this will check if the position currently on the board has been reached
        # for the third time.
        length = len(self.history)

        if length > 6:
            current_position = self.history[length - 1]
            counter = 0
            for j in self.history:
                if j == current_position:
                    counter += 1
            return (counter == 3)
        else:
            return False

    def check_50_move_rule(self):
        # 100, since a 'move' is 2 plys. the clock counts plys.
        return (self.halfmove_clock == 100)

    def translate_to_FEN(self, board):

        FEN_string = ""

        def piece_type(piece):
            try:
                if piece.is_white():
                    return piece.name
                else:
                    return piece.name.lower()
            except:
                return "No piece on the square."

        for j in range(0, 8):
            counter = 0
            for i in range(0, 8):
                # Try except can be sorted
                square_piece = piece_type(board[j][i])
                if square_piece == None:
                    counter += 1
                    if (i == 7):
                        FEN_string += str(counter)
                else:
                    if counter != 0:
                        FEN_string += str(counter)
                        counter = 0
                        FEN_string += square_piece
                    else:
                        FEN_string += square_piece
            FEN_string += "/"
        return FEN_string[0:len(FEN_string) - 1]

    def append_starting_position(self, starting_position):
        self.history.append(self.translate_to_FEN(starting_position))

    def update_gamelog(self, board, reset_halfmove):
        self.history.append(self.translate_to_FEN(board))
        if reset_halfmove:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1
