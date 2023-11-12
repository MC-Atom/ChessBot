from ChessBoard import ChessBoard

# If set to True, allows any piece to be moved regardless of whose turn it is
# Might be useful for faster testing
OVERRIDE_TURN_ORDER = False

def playGame():
    turn = "White"
    board = ChessBoard()
    print("Enter moves by naming the tile to move from and the tile to move to, e.g. a1b3 for a knight move")
    print("Type 'exit' to end the program")
    while True:
        print()
        print(board)
        print("\n" + "=" * 20 + "\n")
        move = input("Enter a move (" + turn + "'s Turn): ")

        if move == "exit":
            exit()

        # Attempt to parse user input into usable board coordinates
        parsedMove = parseMove(move)
        if not parsedMove:
            print("ERROR: Move is badly formatted. Should be [a-f][1-6][a-f][1-6]")
            continue
        
        start, end = parsedMove

        # Check that the piece being moved exists
        piece = board.getPiece(start)
        if piece is None:
            print("ERROR: Invalid move: There is no piece on " + move[:2])
            continue

        # Check that the piece is of the correct color
        if ((turn == "White" and not piece.isWhite()) or (turn == "Black" and piece.isWhite())) \
            and not OVERRIDE_TURN_ORDER:
            print("ERROR: Invalid move: Tried to move a piece of the wrong color")
            continue
        
        # Check if move is valid according to ChessBoard rules
        valid = board.movePiece(piece, end)
        if not valid:
            print("ERROR: Invalid move")
            continue
        
        # Switch turn. Only reachable if no error has occurred
        if turn == "White":
            turn = "Black"
        elif turn == "Black":
            turn = "White"


# Turns user inputted move into board coordinates
# Returns False if invalid formatting
def parseMove(userIn):
    start, end = userIn[:2], userIn[2:]
    start = convertCoordinate(start)
    end = convertCoordinate(end)

    if not (start and end):
        return False

    return (start, end)

# Converts user-input move to board coordinate, e.g. c5 --> (3, 5)
# Returns False if invalid formatting
def convertCoordinate(coord):
    letterToNum = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5}
    try:
        return [letterToNum[coord[0]], int(coord[1]) - 1]
    except:
        return False

if __name__ == '__main__':
    playGame()