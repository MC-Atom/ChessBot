from ChessPiece import ChessPiece

# Gives a material value for each piece type
materialValueMap = {"Pawn": 1, "Knight": 3, "Bishop": 3, "Rook": 5, "Queen": 9, "King": 0}

class ChessBoard:

    def __init__(self):
        self.sizeX = 5 # how many squares wide the board is
        self.sizeY = 6 # how many squares tall the board is
        self.whitePieces = [ChessPiece("Knight",True,(0,0)),ChessPiece("Queen",True,(1,0)),ChessPiece("King",True,(2,0)),ChessPiece("Bishop",True,(3,0)),ChessPiece("Rook",True,(4,0)),
                            ChessPiece("Pawn",True,(0,1)),ChessPiece("Pawn",True,(1,1)),ChessPiece("Pawn",True,(2,1)),ChessPiece("Pawn",True,(3,1)),ChessPiece("Pawn",True,(4,1))]
        self.blackPieces = [ChessPiece("Knight",False,(0,5)),ChessPiece("Queen",False,(1,5)),ChessPiece("King",False,(2,5)),ChessPiece("Bishop",False,(3,5)),ChessPiece("Rook",False,(4,5)),
                            ChessPiece("Pawn",False,(0,4)),ChessPiece("Pawn",False,(1,4)),ChessPiece("Pawn",False,(2,4)),ChessPiece("Pawn",False,(3,4)),ChessPiece("Pawn",False,(4,4))]
        self.board =  [[self.whitePieces[0],self.whitePieces[5],None,None,self.blackPieces[5],self.blackPieces[0]],
                        [self.whitePieces[1],self.whitePieces[6],None,None,self.blackPieces[6],self.blackPieces[1]],
                        [self.whitePieces[2],self.whitePieces[7],None,None,self.blackPieces[7],self.blackPieces[2]],
                        [self.whitePieces[3],self.whitePieces[8],None,None,self.blackPieces[8],self.blackPieces[3]],
                        [self.whitePieces[4],self.whitePieces[9],None,None,self.blackPieces[9],self.blackPieces[4]]]

        # Tracks total material values, is updated on piece death
        self.whiteMaterial, self.blackMaterial = self.evaluateMaterial()

    # Overloaded constructor. Generates a ChessBoard object from a passed in a board matrix
    def __init__(self, board):
        self.sizeX = len(board)
        self.sizeY = len(board[0])
        self.whitePieces = []
        self.blackPieces = []

        for row in board:
            for piece in row:
                if isinstance(piece,ChessPiece):
                    if piece.isWhite():
                        self.whitePieces.append(piece)
                    else:
                        self.blackPieces.append(piece)
        
        # Tracks total material values, is updated on piece death
        self.whiteMaterial, self.blackMaterial = self.evaluateMaterial()


    def movePiece(self, piece, endLoc):
        # Moves a piece from one location to another, overriding the piece at the second location if it exists.
        # Only works if the move is a valid move, function does not move the piece and returns false otherwise.

        if not self.isValidMove(piece, endLoc):
            return False
        
        print("here")
        
        startLoc = piece.getLoc()

        self.board[startLoc[0]][startLoc[1]] = None
        if self.board[endLoc[0]][endLoc[1]] != None:
            self.killPiece(self.board[endLoc[0]][endLoc[1]])
        self.board[endLoc[0]][endLoc[1]] = piece
        piece.moveLoc(endLoc)
        print(piece.getLoc())

        return True

    
    def isValidMove(self, piece, endLoc):
        # Takes in a piece and a tuple (ie. (0,4)) representing an position on the board
        # Returns whether or not the piece type can legally move to the given position

        startLoc = piece.getLoc()
        
        if not self.isValidMoveNoCheck(piece, endLoc):
            return False
        
        # Move the piece, check if it's in check, then move it back.
        tempboard = []
        for column in self.board:
            tempboard.append(column.copy())
        self.board[startLoc[0]][startLoc[1]] = None
        if self.board[endLoc[0]][endLoc[1]] != None:
            self.board[endLoc[0]][endLoc[1]].kill()
        self.board[endLoc[0]][endLoc[1]] = piece
        piece.moveLoc(endLoc)

        if piece.isWhite():
            output = not self.isWhiteInCheck()
        else:
            output = not self.isBlackInCheck()

        print(output)

        self.board = tempboard
        if self.board[endLoc[0]][endLoc[1]] != None:
            self.board[endLoc[0]][endLoc[1]].unkill()
        piece.moveLoc(startLoc)
        return output


    def isValidMoveNoCheck(self, piece, endLoc):
        # Takes in a piece and a tuple (ie. (0,4)) representing an position on the board
        # Returns whether or not the piece type can legally move to the given position
        # Does not take checks into consideration

        startLoc = piece.getLoc()

        if not self.isValidLocation(endLoc) or not self.isValidLocation(startLoc):
            return False
        
        if endLoc == startLoc:
            # Pieces cannot move to the same spot
            return False
        
        if self.getPiece(endLoc) != None and (self.getPiece(endLoc).isWhite() == piece.isWhite()):
            # If there's a piece in the end location and that piece is the same color
            return False

        if piece.pieceType == "Pawn":
            # Takes rules from Quick Chess. Pawns cannot ever move two spaces
            if piece.isWhite():
                if self.getPiece(endLoc) == None: # If there's not a piece there
                    return endLoc[0] == startLoc[0] and endLoc[1] == startLoc[1] + 1
                else: # If there's a piece of the opposite color there
                    return (endLoc[0] == startLoc[0] + 1 or endLoc[0] == startLoc[0] - 1) and endLoc[1] == startLoc[1] + 1
            else: # If the piece isn't white
                if self.getPiece(endLoc) == None: # If there's not a piece there
                    return endLoc[0] == startLoc[0] and endLoc[1] == startLoc[1] - 1
                else: # If there's a piece of the opposite color there
                    return (endLoc[0] == startLoc[0] + 1 or endLoc[0] == startLoc[0] - 1) and endLoc[1] == startLoc[1] - 1
        
        elif piece.pieceType == "King":
            # Takes rules from Quick Chess. Castling is not allowed
            return abs(endLoc[0] - startLoc[0]) <= 1 and abs(endLoc[1] - startLoc[1]) <= 1 and endLoc != startLoc
        
        elif piece.pieceType == "Queen":
            if endLoc[0] == startLoc[0]: # If it's moving up/down
                for i in range (min(endLoc[0],startLoc[0])+1,max(endLoc[0],startLoc[0])):
                    if self.getPiece((i,endLoc[1])) != None: # If there are pieces between the starting pos and ending pos
                        return False
                return True
            elif endLoc[1] == startLoc[1]: # If it's moving left/right
                for i in range (min(endLoc[1],startLoc[1])+1,max(endLoc[1],startLoc[1])):
                    if self.getPiece((i,endLoc[0])) != None: # If there are pieces between the starting pos and ending pos
                        return False
                return True
            elif endLoc[0] - startLoc[0] == endLoc[1] - startLoc[1]: # If it's moving along y = x
                for i in range(1,abs(endLoc[0]-startLoc[0])):
                    if self.getPiece(min(endLoc[0],startLoc[0])+i,min(endLoc[1],startLoc[1])+i) is not None:
                        return False
                return True
            elif endLoc[0] - startLoc[0] == -(endLoc[1] - startLoc[1]): # If it's moving along y = -x
                for i in range(1,abs(endLoc[0]-startLoc[0])):
                    if self.getPiece((min(endLoc[0],startLoc[0])+i,max(endLoc[1],startLoc[1])-i)) is not None:
                        return False
            else:
                return False
            
        elif piece.pieceType == "Knight":
            print("KINIGHT!!!!")
            return (abs(endLoc[0] - startLoc[0]) == 2 and abs(endLoc[1] - startLoc[1]) == 1) or \
                    (abs(endLoc[0] - startLoc[0]) == 1 and abs(endLoc[1] - startLoc[1]) == 2)
        
        elif piece.pieceType == "Rook":
            if endLoc[0] == startLoc[0]: # If it's moving up/down
                for i in range (min(endLoc[0],startLoc[0])+1,max(endLoc[0],startLoc[0])):
                    if self.getPiece((i,endLoc[1])) != None: # If there are pieces between the starting pos and ending pos
                        return False
                return True
            elif endLoc[1] == startLoc[1]: # If it's moving left/right
                for i in range (min(endLoc[1],startLoc[1])+1,max(endLoc[1],startLoc[1])):
                    if self.getPiece((i,endLoc[0])) != None: # If there are pieces between the starting pos and ending pos
                        return False
                return True
            else:
                return False

        elif piece.pieceType == "Bishop":
            if endLoc[0] - startLoc[0] == endLoc[1] - startLoc[1]: # If it's moving along y = x
                for i in range(1,abs(endLoc[0]-startLoc[0])):
                    if self.getPiece((min(endLoc[0],startLoc[0])+i,min(endLoc[1],startLoc[1])+i)) is not None:
                        return False
                return True
            elif endLoc[0] - startLoc[0] == -(endLoc[1] - startLoc[1]): # If it's moving along y = -x
                for i in range(1,abs(endLoc[0]-startLoc[0])):
                    if self.getPiece(min(endLoc[0],startLoc[0])+i,max(endLoc[1],startLoc[1])-i) is not None:
                        return False
            else:
                return False
        
        else:
            return False
    
    def getPiece(self,location):
        # Returns the piece in the given location or returns None if no piece is there or if it's an invalid lcoation
        if not self.isValidLocation(location):
            return None
        
        return self.board[location[0]][location[1]]

    def isValidLocation(self, location):
        # Checks whether or not the given location is on the game board
        return location[0] >= 0 and location[1] >= 0 and location[0] < self.sizeX and location[1] < self.sizeY
    
    def isWhiteInCheck(self):
        # Checks the current game board for whether or not the white king is in check
        for piece in self.whitePieces:
            if piece.getPieceType() == "King":
                kingPos = piece.getLoc()
                break
        
        for piece in self.blackPieces:
            if piece.isAlive() and self.isValidMoveNoCheck(piece,kingPos):
                return True
        return False
    
    def isBlackInCheck(self):
        # Checks the current game board for whether or not the black king is in check
        for piece in self.blackPieces:
            if piece.getPieceType() == "King":
                kingPos = piece.getLoc()
                break
        
        for piece in self.whitePieces:
            if piece.isAlive() and self.isValidMoveNoCheck(piece,kingPos):\
                return True
        return False

    # Kills the piece and removes its material value from its player's total
    # TODO: Should this method remove the piece from its players piece list?
    def killPiece(self, piece):
        piece.kill()

        pieceValue = materialValueMap[piece.pieceType]
        if piece.isWhite():
            self.whiteMaterial -= pieceValue
        else:
            self.blackMaterial -= pieceValue
    
    # Returns a tuple (whiteMaterial, blackMaterial), which is the total material
    # value of each player on this board
    def evaluateMaterial(self):
        whiteMaterial = sum([materialValueMap[piece.pieceType] for piece in self.whitePieces])
        blackMaterial = sum([materialValueMap[piece.pieceType] for piece in self.blackPieces])
        return (whiteMaterial, blackMaterial)
    
    def getBoard(self):
        return self.board
    
    def __str__(self):
        output = "   | "
        for i in range(self.sizeX):
            output += chr(i + 65)
            output += " | "
        
        for j in range(self.sizeY):
            output += "\n"
            output += "-------------------------\n"
            output += str(j+1) + "  |"
            for i in range(self.sizeX):
                if self.board[i][j] != None:
                    output += self.board[i][j]
                else:
                    output += "  "
                output += " |"
        output += "\n"
        output += "-------------------------"
        return output