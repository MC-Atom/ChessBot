class ChessPiece:

    def __init__(self, pieceType, isWhite, location):
        self.pieceType = pieceType # A string that should only be one of "Pawn", "King", "Queen", "Knight", "Rook", "Bishop"
        self.isWhite = isWhite # True if the piece is white, False otherwise (if the piece is black)
        self.location = location
        self.isAlive = True

    def isWhite(self):
        return self.isWhite
  
    def getPieceType(self):
        return self.pieceType

    def getLoc(self):
        return self.location

    def moveLoc(self, newLoc):
        self.location = newLoc
    
    def kill(self):
        self.isAlive = False
    
    def unkill(self):
        self.isAlive = True

    def isAlive(self):
        return self.isAlive

    def toString(self):
        output = ""
        if self.isWhite:
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