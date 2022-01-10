#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#This will take a current position and return possible moves.
#I really should have done this before implimenting stalemate and checkmate tbh!
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def move_finder(board):
    move_list = []
    colour_to_move = board.white_to_move

    for i in range(0,8):
        for j in range(0,8):
            #Go through board to find correct pieces
            if board.board[j][i] != None:
                if (board.board[j][i].is_white() == colour_to_move):
                    #Go through board to see where these pieces can move.
                    for k in range(0,8):
                        for l in range(0,8):
                            if (board.valid_move(board.board, (i,j), (k,l)) == True):
                                if (board.check_self_discovery((i,j), (k,l)) == False):
                                    move_list.append([(i,j), (k,l)])
                                    
    return move_list

def piece_move_finder(board, square):
    move_list = []
    
    for i in range(0,8):
        for j in range(0,8):
            if (board.valid_move(board.board, square, (i,j)) == True):
                if (board.check_self_discovery(square, (i,j)) == False):
                    move_list.append((i,j))

    return move_list