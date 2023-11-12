from ChessBoard import ChessBoard

def playGame():
    turn = "White"
    board = ChessBoard()
    print("Enter moves by naming the tile to move from and the tile to move to, e.g. a1b3 for a knight move")
    while True:
        print()
        print(board)
        print("\n" + "=" * 20 + "\n")
        move = input("Enter a move: ")

        parsedMove = parseMove(move)
        if not parsedMove:
            print("ERROR: Move is badly formatted. Should be [a-f][1-6][a-f][1-6]")
            continue
        
        start, end = parsedMove

        piece = board.getPiece(start)
        if piece is None:
            print("ERROR: Invalid move: There is no piece on " + move[:2])
            continue
            
        print(piece.pieceType)
        
        valid = board.movePiece(piece, end)
        if not valid:
            print("ERROR: Invalid move")


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