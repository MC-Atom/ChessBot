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

    def promote(self, type="Queen"):
        self.pieceType = type

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
        if not self.isAlive():
            return []
    
        validMoves = []

        if self.pieceType == "Pawn":
            # Takes rules from Quick Chess. Pawns cannot ever move two spaces
            if self.isWhite():
                # Check if there's a piece in front of the pawn
                if board.getPiece((self.location[0],self.location[1]+1)) == None: 
                    validMoves.append((self.location[0],self.location[1]+1))
                
                # Check if there's an enemy piece on either side of the pawn
                if board.getPiece((self.location[0]-1,self.location[1]+1)) != None \
                and board.getPiece((self.location[0]-1,self.location[1]+1)).isWhite() != self.isWhite:
                    validMoves.append((self.location[0]-1,self.location[1]+1))

                if board.getPiece((self.location[0]+1,self.location[1]+1)) != None \
                and board.getPiece((self.location[0]+1,self.location[1]+1)).isWhite() != self.isWhite:
                    validMoves.append((self.location[0]+1,self.location[1]+1))
            
            else:
                # Check if there's a piece in front of the pawn
                if board.getPiece((self.location[0],self.location[1]-1)) == None: 
                    validMoves.append((self.location[0],self.location[1]-1))
                
                # Check if there's an enemy piece on either side of the pawn
                if board.getPiece((self.location[0]-1,self.location[1]-1)) != None \
                and board.getPiece((self.location[0]-1,self.location[1]-1)).isWhite() != self.isWhite:
                    validMoves.append((self.location[0]-1,self.location[1]-1))

                if board.getPiece((self.location[0]+1,self.location[1]-1)) != None \
                and board.getPiece((self.location[0]+1,self.location[1]-1)).isWhite() != self.isWhite:
                    validMoves.append((self.location[0]+1,self.location[1]-1))
        
        elif self.pieceType == "King":
            # Takes rules from Quick Chess. Castling is not allowed

            # Add all adjacent spaces. 
            # Checks for pieces in those spaces and whether or not they are on the board are done later
            validMoves.append((self.location[0]+1,self.location[1]+1))
            validMoves.append((self.location[0],self.location[1]+1)) 
            validMoves.append((self.location[0]-1,self.location[1]+1))
            validMoves.append((self.location[0]-1,self.location[1]))
            validMoves.append((self.location[0]-1,self.location[1]-1))
            validMoves.append((self.location[0],self.location[1]-1))
            validMoves.append((self.location[0]+1,self.location[1]-1))
            validMoves.append((self.location[0]+1,self.location[1]))
        
        elif self.pieceType == "Queen":
            directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

            # The piece can move in one of 8 directions
            for direction in directions:
                xDif = direction[0]
                yDif = direction[1]

                endLoc = (self.location[0]+xDif,self.location[1]+yDif)
                validMoves.append(endLoc)

                # Add all spaces between the piece's location and another piece or an edge of the board
                while (board.getPiece(endLoc) == None and board.isValidLocation(endLoc)):

                    xDif += direction[0]
                    yDif += direction[1]
                    endLoc = (self.location[0]+xDif,self.location[1]+yDif)
                    validMoves.append(endLoc)
        
        # Just add all the possible spots a knight can go, sort out whether or not they are correct at the end
        elif self.pieceType == "Knight":
            validMoves.append((self.location[0]+1,self.location[1]+2))
            validMoves.append((self.location[0]-1,self.location[1]+2))
            validMoves.append((self.location[0]-1,self.location[1]-2))
            validMoves.append((self.location[0]+1,self.location[1]-2))

            validMoves.append((self.location[0]+2,self.location[1]+1))
            validMoves.append((self.location[0]-2,self.location[1]+1))
            validMoves.append((self.location[0]-2,self.location[1]-1))
            validMoves.append((self.location[0]+2,self.location[1]-1))
        
        elif self.pieceType == "Rook":
            directions = [(0,1),(1,0),(0,-1),(-1,0)]

            # The piece can move in one of 4 directions
            for direction in directions:
                xDif = direction[0]
                yDif = direction[1]

                endLoc = (self.location[0]+xDif,self.location[1]+yDif)
                validMoves.append(endLoc)

                # Add all spaces between the piece's location and another piece or an edge of the board
                while (board.getPiece(endLoc) == None and board.isValidLocation(endLoc)):

                    xDif += direction[0]
                    yDif += direction[1]
                    endLoc = (self.location[0]+xDif,self.location[1]+yDif)
                    validMoves.append(endLoc)

        elif self.pieceType == "Bishop":
            directions = [(1,1),(1,-1),(-1,1),(-1,-1)]

            # The piece can move in one of 4 directions
            for direction in directions:
                xDif = direction[0]
                yDif = direction[1]

                endLoc = (self.location[0]+xDif,self.location[1]+yDif)
                validMoves.append(endLoc)

                # Add all spaces between the piece's location and another piece or an edge of the board
                while (board.getPiece(endLoc) == None and board.isValidLocation(endLoc)):

                    xDif += direction[0]
                    yDif += direction[1]
                    endLoc = (self.location[0]+xDif,self.location[1]+yDif)
                    validMoves.append(endLoc)
        
        #print("\033[33m",self,validMoves,"\033[0m")

        validMovesChecked = []
        for endLoc in validMoves:
            """
            # Old functions
            # Check to make sure the end location is empty or has an enemy piece in it
            if board.getPiece(endLoc) == None or (board.getPiece(endLoc).isWhite() != self.isWhite()):
                # Check to make sure the end location is within the bounds of the board
                if board.isValidLocation(endLoc):
                    validMovesChecked.append(endLoc)
            """

            # Checks if the move is a valid move (checks if it's in check among other things)
            if board.isValidMove(self,endLoc):
                validMovesChecked.append(endLoc)
        
        #print("\033[32m",self,validMovesChecked,"\033[0m")
        return validMovesChecked
    
    