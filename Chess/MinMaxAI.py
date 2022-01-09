#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#An AI which maximises a very simple evaluation score (based on material and piece square tables)
#in position after making a single move.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import MoveFinder
import Evaluation
import copy

class MinMaxAI:
    def __init__(self):
        depth = ""
        valid = False
        while (not valid):
            depth = input("What depth would you like the AI to search? ")
            try:
                depth = int(depth)
                if (depth in [1,2,3,4]):
                    valid = True
            except:
                print("Not a valid input. Please input 1,2,3 or 4.")
        self.depth = depth
        self.evaluator = Evaluation.Evaluator("simple")


    def one_deep_search_score(self, board): #THIS WILL BE RENAMED SINCE THIS IS CURRENTLY ONLY A SINGLE DEPTH SEARCH. JUST FOR TESTING.
        #Performs a one deep minmax search.
        movelist = MoveFinder.move_finder(board)
        colour = board.board[movelist[0][0][1]][movelist[0][0][0]].is_white()
        colour_multiplier = 1 if colour else -1
        scores = []
        for i in movelist:
            next_scores = []
            workingboard = copy.deepcopy(board)
            workingboard.move(i[0], i[1])
            workingboard.white_to_move = not workingboard.white_to_move
            if workingboard.check_for_mate():
                scores.append(99999)
                continue

            next_movelist = MoveFinder.move_finder(workingboard)

            for j in next_movelist:
                next_workingboard = copy.deepcopy(workingboard)
                next_workingboard.move(j[0],j[1])
                next_workingboard.white_to_move = not next_workingboard.white_to_move
                if next_workingboard.check_for_mate():
                    next_scores.append(-99999 * colour_multiplier)
                else:
                    next_scores.append(self.evaluator.evaluate_board(next_workingboard.board))

            if min([score * colour_multiplier for score in next_scores]) > 50:
                return min([score * colour_multiplier for score in next_scores])
            scores.append(min([score * colour_multiplier for score in next_scores]))

        return max(scores)

    def n_deep_search(self, board, n):
        if (n > 1):
            #Find AI moves
            movelist = MoveFinder.move_finder(board)
            scores = []
            for i in movelist:
                workingboard = copy.deepcopy(board)
                next_scores = []
                workingboard.move(i[0], i[1])
                workingboard.white_to_move = not workingboard.white_to_move
                if workingboard.check_for_mate():
                    scores.append(99999)
                    continue
                elif workingboard.check_for_stalemate():
                    scores.append(0)
                
                next_movelist = MoveFinder.move_finder(workingboard)

                for j in next_movelist:
                    next_workingboard = copy.deepcopy(workingboard)
                    next_workingboard.move(j[0],j[1])
                    next_workingboard.white_to_move = not next_workingboard.white_to_move
                    if next_workingboard.check_for_mate():
                        next_scores.append(-99999)
                    elif next_workingboard.check_for_stalemate():
                        next_scores.append(0)
                    else:
                        next_scores.append(self.n_deep_search(next_workingboard, n-1))
                if min(next_scores) > 60:
                    scores.append(min(next_scores))
                    if n == self.depth:
                        return movelist[scores.index(min(next_scores))]
                    else:
                        return min(next_scores)
                scores.append(min(next_scores))

            if n == self.depth:
                return movelist[scores.index(max(scores))]
            else:
                return max(scores)
        else:
            return self.one_deep_search_score(board) #THIS CODE NOW FAILS IF N=1 OH NO!

    def move(self, board):
        return self.n_deep_search(board, self.depth)