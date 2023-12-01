from ChessBoard import ChessBoard
from ChessPiece import Chesspiece

class Bot:

    def __init__(self,isWhite,board):
        self.isWhite = isWhite
        self.score = 0
        self.board = board

    # Best fit heuristic to evaluate numerical position
    def calcScore(self, board):
        score = board.evaluateMaterial() # counts taken piece values

        if (self.board.isBlackInCheck(self)):
            if self.isWhite:
                score *= 1.25
            else:
                score *= 0.75
                

        if (self.board.isWhiteInCheck(self)):
            if self.isWhite:
                score *= 0.75
            else:
                score *= 1.25

        

        return score

    def nextMove(self,board):
        pieces = board.whitePieces if self.isWhite else board.blackPieces

        possibleMoves = []
        bestMove = None

        for piece in pieces:
            moves = piece.getValidMoves()
            for move in moves:
                newBoard = ChessBoard(board.getBoard)
                newBoard.movePiece(piece,move)

                moveScore = self.calcScore(self,newBoard)
                newMove = PossibleMove(board,piece,move,moveScore)

                possibleMoves.append(newMove)

                if bestMove == None:
                    bestMove = newMove
                elif (bestMove.score < newMove):
                    bestMove = newMove
        
        return bestMove



class PossibleMove:
    def __init__(self,board,score,piece,endPos,parent):
        self.board = board
        self.piece = piece
        self.endPos = endPos
        self.score = score

        self.parent = parent
        self.childList = []


