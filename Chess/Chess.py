#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#Responsible for game logic.
#I have copy and pasted a large chunk of code a couple of times... Please don't judge my poor coding.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import Board
import GameLog
import MoveGenerator

class Chess():
    def __init__(self):
        self.board = Board.Board()

def translate(coord):
    try:
        file = coord[0]
        rank = coord[1]
        dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f':5, 'g':6, 'h':7}

        rank = int(rank)
        if rank < 1 or rank > 8:
            return None
        else:
            return (dict[file], 8 - rank)
    except:
        return None


def PvP():
    chess = Chess()
    gamelog = GameLog.GameLog()
    gamelog.append_starting_position(chess.board.board)
    start = ""
    end = ""
    chess.board.print_board()
    while (True):
        start = input("Start: ")
        ###TEMPORARY SOLUTION TO QUITTING THE GAME
        if start == "quit":
            quit()

        end = input("End: ")

        ###TEMPORARY SOLUTION TO QUITTING THE GAME
        if end == "quit":
            quit()

        start = translate(start)
        end = translate(end)

        if start == None or end == None:
            print("Not a valid start or end entry.")
            continue
        
        if (chess.board.valid_move(chess.board.board, start, end) == True):
            if (chess.board.check_self_discovery(start, end) == False):
                chess.board.move(start, end)
                chess.board.white_to_move = not chess.board.white_to_move
                gamelog.update_gamelog(chess.board.board, chess.board.reset_halfmove_clock)
        else:
            continue
        
        chess.board.print_board()

        if chess.board.check_for_mate():
            if chess.board.white_to_move:
                message = "Checkmate. Black wins."
            else:
                message = "Checkmate. White wins."

            print(message)
            while (True):
                play_again = input("Play again? (Y/N) ")
                if play_again == "Y":
                    chess = Chess()
                    gamelog = GameLog.GameLog()
                    start = ""
                    end = ""
                    chess.board.print_board()
                    break
                elif play_again == "N":
                    quit()
                else:
                    continue

        if (gamelog.check_50_move_rule() | gamelog.check_for_repetition() | chess.board.check_for_stalemate()):
            print("A draw.")
            while (True):
                play_again = input("Play again? (Y/N) ")
                if play_again == "Y":
                    chess = Chess()
                    gamelog = GameLog.GameLog()
                    start = ""
                    end = ""
                    chess.board.print_board()
                    break
                elif play_again == "N":
                    quit()
                else:
                    continue

def Player_to_move(chess):
    player_moved = False

    while (player_moved == False):
        start = input("Start: ")
        ###TEMPORARY SOLUTION TO QUITTING THE GAME
        if start == "quit":
            quit()

        end = input("End: ")

        ###TEMPORARY SOLUTION TO QUITTING THE GAME
        if end == "quit":
            quit()

        start = translate(start)
        end = translate(end)

        if start == None or end == None:
            print("Not a valid start or end entry.")
            continue
        
        if (chess.board.valid_move(chess.board.board, start, end) == True):
            if (chess.board.check_self_discovery(start, end) == False):
                chess.board.move(start, end)
                player_moved = True
        else:
            continue

def Computer_to_move(chess, computer):
    computer.move(chess.board)


def PvC(player_colour):
    match player_colour:
        case 'w':
            parity = 0
        case 'b':
            parity = 1

    chess = Chess()
    gamelog = GameLog.GameLog()
    gamelog.append_starting_position(chess.board.board)
    
    #Choose your fighter
    while (True):
        ai = input("Enter name of AI you would like to challenge: ")
        if (ai in MoveGenerator.get_list_of_AI()):
            computer = MoveGenerator.MoveGenerator(ai)
            break

    chess.board.print_board()

    while (True):
        if (parity == 0):
            Player_to_move(chess)
            parity = 1
        else:
            Computer_to_move(chess, computer)
            parity = 0

        chess.board.white_to_move = not chess.board.white_to_move
        gamelog.update_gamelog(chess.board.board, chess.board.reset_halfmove_clock)
        chess.board.print_board()

        if chess.board.check_for_mate():
            if chess.board.white_to_move:
                message = "Checkmate. Black wins."
            else:
                message = "Checkmate. White wins."

            print(message)
            while (True):
                play_again = input("Play again? (Y/N) ")
                if play_again == "Y":
                    chess = Chess()
                    gamelog = GameLog.GameLog()
                    start = ""
                    end = ""
                    chess.board.print_board()
                    break
                elif play_again == "N":
                    quit()
                else:
                    continue

        if (gamelog.check_50_move_rule() | gamelog.check_for_repetition() | chess.board.check_for_stalemate()):
            print("A draw.")
            while (True):
                play_again = input("Play again? (Y/N) ")
                if play_again == "Y":
                    chess = Chess()
                    gamelog = GameLog.GameLog()
                    start = ""
                    end = ""
                    chess.board.print_board()
                    break
                elif play_again == "N":
                    quit()
                else:
                    continue
def main():
    while (True):
        game_type = input("Press 1 for PvP, press 2 to play against AI as white, and press 3 to play against AI as black. ")
        match game_type:
            case "1":
                PvP()
            case "2":
                PvC('w')
            case "3":
                PvC('b')

if __name__ == "__main__":
    main()