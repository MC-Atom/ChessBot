from ChessBoard import ChessBoard
from ChessPiece import Chesspiece

class Bot:

    def nextMove(self,board):
        pieces = board.whitePieces if self.isWhite else board.blackPieces

        for piece in pieces:
            moves = piece.getValidMoves()
            for move in moves:
                newBoard = ChessBoard(board.getBoard)
                newBoard.movePiece(piece,move)

                moveScore = self.calcScore(self,newBoard)

class PossibleMove:
    def __init__(self,board,piece,endPos,parent):
        self.board = board
        self.piece = piece
        self.endPos = endPos

        self.parent = parent
        childList = []