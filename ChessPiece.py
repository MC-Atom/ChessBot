class ChessPiece:

    def __init__(self, pieceType, isWhite, location):
        self.pieceType = pieceType # A string that should only be one of "Pawn", "King", "Queen", "Knight", "Rook", "Bishop"
        self.white = isWhite # True if the piece is white, False otherwise (if the piece is black)
        self.location = location
        self.alive = True

    def isWhite(self):
        return self.white
  
    def getPieceType(self):
        return self.pieceType

    def getLoc(self):
        return self.location

    def moveLoc(self, newLoc):
        self.location = newLoc
    
    def kill(self):
        self.alive = False
    
    def unkill(self):
        self.alive = True

    def isAlive(self):
        return self.alive

    def __str__(self):
        output = ""
        if self.white:
            output += "W"
        else:
            output += "B"
        
        if self.pieceType == "Pawn":
            output += "p"
        elif self.pieceType == "King":
            output += "k"
        elif self.pieceType == "Queen":
            output += "q"
        elif self.pieceType == "Knight":
            output += "n"
        elif self.pieceType == "Rook":
            output += "r"
        elif self.pieceType == "Bishop":
            output += "b"
        
        return output
    
    # Returns a list of tuples representing all moves the piece can make on the given board
    def getValidMoves(self,board):
        validMoves = []

        if self.pieceType == "Pawn":
            # Takes rules from Quick Chess. Pawns cannot ever move two spaces
            if self.isWhite():
                endLoc = (self.location[0],self.location+1)
                if board.getPiece(endLoc) == None: # If there isn't a piece ahead of the pawn
                    validMoves.append(endLoc)

                if board.getPiece(endLoc) == None: # If there's not a piece there
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
        
        validMovesChecked = []
        for endLoc in validMoves:
            # Check to make sure the end location is empty or has an enemy piece in it
            if board.getPiece(endLoc) == None or (board.getPiece(endLoc).isWhite() != self.isWhite()):
                # Check to make sure the end location is within the bounds of the board
                if board.isValidLocation(endLoc):
                    validMovesChecked.append(endLoc)

        return validMoves
    
    