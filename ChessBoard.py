import ChessPiece

class ChessBoard:

    def __init__(self):
        self.sizeX = 5 # how many squares wide the board is
        self.sizeY = 6 # how many squares tall the board is
        self.whitePieces = [ChessPiece("Knight",True),ChessPiece("Queen",True),ChessPiece("King",True),ChessPiece("Bishop",True),ChessPiece("Rook",True),
                            ChessPiece("Pawn",True),ChessPiece("Pawn",True),ChessPiece("Pawn",True),ChessPiece("Pawn",True),ChessPiece("Pawn",True)]
        self.blackPieces = [ChessPiece("Knight",False),ChessPiece("Queen",False),ChessPiece("King",False),ChessPiece("Bishop",False),ChessPiece("Rook",False),
                            ChessPiece("Pawn",False),ChessPiece("Pawn",False),ChessPiece("Pawn",False),ChessPiece("Pawn",False),ChessPiece("Pawn",False)]
        self.board =  [[self.whitePieces[0],self.whitePieces[1],self.whitePieces[2],self.whitePieces[3],self.whitePieces[4]],
                       [self.whitePieces[5],self.whitePieces[6],self.whitePieces[7],self.whitePieces[8],self.whitePieces[9]],
                       [None,None,None,None,None],
                       [None,None,None,None,None],
                       [self.blackPieces[5],self.blackPieces[6],self.blackPieces[7],self.blackPieces[8],self.blackPieces[9]],
                       [self.blackPieces[0],self.blackPieces[1],self.blackPieces[2],self.blackPieces[3],self.blackPieces[4]]]
    
    def isValidMove(self, piece, endLoc):

        startLoc = piece.getLoc()
        
        if not self.isValidMoveNoCheck(self, piece, endLoc):
            return False
        
        # Move the piece, check if it's in check, then move it back.
        tempboard = self.board.copy()
        self.board[startLoc[0]][startLoc[1]] = None
        self.board[endLoc[0]][endLoc[1]] = piece
        piece.moveLoc(endLoc)
        if piece.isWhite():
            output = self.isWhiteInCheck()
        else:
            output = self.isBlackInCheck()
        
        self.board = tempboard
        piece.moveLoc(startLoc)
        return output


    def isValidMoveNoCheck(self, piece, endLoc):
        # Takes in two two value long tuples (ie. (0,4)) representing positions on the board
        # Returns whether or not the piece type can legally make that move
        # Does not take checks into consideration

        startLoc = piece.getLoc()

        if not self.isValidLocation(endLoc) or not self.isValidLocation(startLoc):
            return False
        
        if endLoc == startLoc:
            # Pieces cannot move to the same spot
            return False
        
        if self.getPiece(endLoc) != None and (self.getPiece(endLoc).isWhite() == piece.isWhite):
            # If there's a piece in the end location and that piece is the same color
            return False

        if piece.pieceType == "Pawn":
            # Takes rules from Quick Chess. Pawns cannot ever move two spaces
            if piece.isWhite():
                if self.getPiece(endLoc) == None: # If there's not a piece there
                    return endLoc[0] == startLoc[0] and endLoc[1] == startLoc[1] - 1
                else: # If there's a piece of the opposite color there
                    return (endLoc[0] == startLoc[0] + 1 or endLoc[0] == startLoc[0] - 1) and endLoc[1] == startLoc[1] - 1
            else: # If the piece isn't white
                if self.getPiece(endLoc) == None: # If there's not a piece there
                    return endLoc[0] == startLoc[0] and endLoc[1] == startLoc[1] + 1
                else: # If there's a piece of the opposite color there
                    return (endLoc[0] == startLoc[0] + 1 or endLoc[0] == startLoc[0] - 1) and endLoc[1] == startLoc[1] + 1
        
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
                    if self.getPiece(min(endLoc[0],startLoc[0])+i,max(endLoc[1],startLoc[1])-i) is not None:
                        return False
            else:
                return False
            
        elif piece.pieceType == "Knight":
            return (abs(endLoc[0] - startLoc[0]) == 3 and abs(endLoc[1] - startLoc[1]) == 2) or \
                    (abs(endLoc[0] - startLoc[0]) == 2 and abs(endLoc[1] - startLoc[1]) == 3)
        
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
                    if self.getPiece(min(endLoc[0],startLoc[0])+i,min(endLoc[1],startLoc[1])+i) is not None:
                        return False
                return True
            elif endLoc[0] - startLoc[0] == -(endLoc[1] - startLoc[1]): # If it's moving along y = -x
                for i in range(1,abs(endLoc[0]-startLoc[0])):
                    if self.getPiece(min(endLoc[0],startLoc[0])+i,max(endLoc[1],startLoc[1])-i) is not None:
                        return False
            else:
                return False
    
    def getPiece(self,location):
        # Returns the piece in the given location or returns None if no piece is there or if it's an invalid lcoation
        if not self.isValidLocation(location):
            return None
        
        return self.board[location[1]][location[0]]

    def isValidLocation(self, location):
        # Checks whether or not the given location is on the game board
        return location[0] >= 0 and location[1] >= 0 and location[0] < self.sizeX and location[1] < self.sizeY
    
    def isWhiteInCheck(self):
        # Checks the current game board for whether or not the white king is in check
        for piece in self.whitePieces:
            if piece.getPieceType() == "King":
                whiteKingPos = piece.getPos()
                break
        
        for piece in self.blackPieces:
            if self.isValidMoveNoCheck(piece,whiteKingPos):
                return True
        return False
    
    def isBlackInCheck(self):
        # Checks the current game board for whether or not the black king is in check
        for piece in self.blackPieces:
            if piece.getPieceType() == "King":
                whiteKingPos = piece.getPos()
                break
        
        for piece in self.whitePieces:
            if self.isValidMoveNoCheck(piece,whiteKingPos):
                return True
        return False
    