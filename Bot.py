from Chessboard import ChessBoard
from Chesspiece import Chesspiece

self.isWhite = true
self.score = 0
self.board = ChessBoard() #generate fresh board

# Best fit heuristic to evaluate numerical position
def calcScore(self, board):
    self.score = board.evaluateMaterial() # counts taken piece values

    if (self.board.isBlackInCheck(self)):
        if self.isWhite:
            self.score *= 1.25
        else:
            self.score *= 0.75
            

    if (self.board.isWhiteInCheck(self)):
        if !self.isWhite:
            self.score *= 1.25
        else:
            self.score *= 0.75

     

    return score

