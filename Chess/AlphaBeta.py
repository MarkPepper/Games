#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#My MinMaxAI was very slow (about 15mins to make an opening move)
#Here is the alpha beta pruning version. α β
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import MoveFinder
import MoveGenerator
import Evaluation
import copy

class AlphaBeta():
    def __init__(self):
        depth = ""
        valid = False
        while (not valid):
            depth = input("What depth would you like the AI to search? ")
            try:
                depth = int(depth)
                if (depth in [1,2,3,4,5,6,7,8]):
                    valid = True
            except:
                print("Not a valid input. Please input 1,2,3 or 4.")
        self.depth = depth
        self.evaluator = Evaluation.Evaluator("simple")
        self.infinity = 9999999

    def alpha_beta_algorithm(self, board, depth, α, β, maximizingPlayer, col_multiplier):
        #quickly check that none of the following moves will instantly result in checkmate.
        movelist = MoveFinder.move_finder(board)
        if (len(movelist) == 0):
            if board.check_for_mate():
                if maximizingPlayer:
                    return [-self.infinity, 0]
                else:
                    return [self.infinity, 0]
            elif board.check_for_stalemate():
                return [0,0]
                
        if (depth == 0): #OR IF THIS IS  TERMINAL NODE. NEED TO CHANGE EVALUATION TO GIVE A SCORE IN CHECKMATE/DRAW SITUATIONS
            return [col_multiplier * self.evaluator.evaluate_board(board.board), 0]

        

        if maximizingPlayer:
            value = -self.infinity
            movelist = MoveFinder.move_finder(board)
            current_move = movelist[0]
            for moves in movelist:
                next_board = copy.deepcopy(board)
                next_board.move(moves[0], moves[1])
                next_board.white_to_move = not next_board.white_to_move
                old_value = value
                value = max([value, self.alpha_beta_algorithm(next_board, depth - 1, α, β, False, col_multiplier)[0]])
                if value >= β:
                    break
                if (old_value != value):
                    current_move = moves
                α = max([α, value])
            return [value, current_move]

        else:
            value = self.infinity
            movelist = MoveFinder.move_finder(board)
            current_move = movelist[0]
            for moves in movelist:
                next_board = copy.deepcopy(board)
                next_board.move(moves[0],moves[1])
                next_board.white_to_move = not next_board.white_to_move
                old_value = value
                value = min([value, self.alpha_beta_algorithm(next_board, depth - 1, α, β, True, col_multiplier)[0]])
                if value <= α:
                    break
                if (old_value != value):
                    current_move = moves
                β = min([β, value])
            return [value, current_move]


        
    def move(self, board):
        moves = MoveFinder.move_finder(board)
        if board.board[moves[0][0][1]][moves[0][0][0]].is_white():
            multiplier = 1
        else:
            multiplier = -1

        return self.alpha_beta_algorithm(board, self.depth, - self.infinity, self.infinity, True, multiplier)[1]
