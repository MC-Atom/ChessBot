class ChessPiece:

    def __init__(self, pieceType, isWhite, position):
        self.pieceType = pieceType # A string that should only be one of "Pawn", "King", "Queen", "Knight", "Rook", "Bishop"
        self.isWhite = isWhite # True if the piece is white, False otherwise (if the piece is black)
        self.position = position
        self.isAlive = True

    def isWhite(self):
        return self.isWhite
  
    def getPieceType(self):
        return self.pieceType

    def getPos(self):
        return self.position

    def movePos(self, newPos):
        return self.position = newPos
    
    def kill(self):
        self.isAlive = False
    
    def isAlive(self):
        return self.isAlive
  
  
          