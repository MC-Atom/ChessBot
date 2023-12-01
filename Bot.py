from Chessboard import ChessBoard
from Chesspiece import Chesspiece

self.score = 0
self.board = ChessBoard() #generate fresh board

# Best fit heuristic to evaluate numerical position
def update(self,board):
    self.score = board.evaluateMaterial()
    
