#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#Provides chess with the AI moves. This page is not itself an AI.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import RandomAI
import MinMaxAI

def get_list_of_AI():
    return ["random", "minmax"]

class MoveGenerator():
    def __init__(self, AI_choice):
        match AI_choice:
            case "random":
                self.AI = RandomAI.RandomAI()
            case "minmax":
                self.AI = MinMaxAI.MinMaxAI()

    def move(self, board):
        [start, end] = self.AI.move(board)
        board.move(start, end)