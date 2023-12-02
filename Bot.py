import copy
import random
from ChessPiece import ChessPiece

class Bot:
    RANDOM_MULT = 0.025
    SHOW_THINKING = False

    def __init__(self,isWhite,board):
        self.isWhite = isWhite
        self.board = board

    # Best fit heuristic to evaluate numerical position
    def calcScore(self, board, isWhite):
        whiteMaterial, blackMaterial = board.evaluateMaterial() # counts taken piece values

        # add a 100 point buffer so the score doesn't go negative 
        if isWhite:
            score = 100 + whiteMaterial - blackMaterial
        else:
            score = 100 + blackMaterial - whiteMaterial
        
        if score < 0:
            print("ERROR: SCORE LESS THAN ZERO")

        if (self.board.isBlackInCheck()):
            if isWhite:
                score *= 1.25
            else:
                score *= 0.75
                

        if (self.board.isWhiteInCheck()):
            if isWhite:
                score *= 0.75
            else:
                score *= 1.25

        # multiplies by 1 +/- at most the random multiplier for randomness
        score *= 1 + (random.random() * self.RANDOM_MULT * 2) - self.RANDOM_MULT

        return score

    # Formats the next move
    def nextMoveFormated(self,board):
        nextMove = self.nextMoveInternal(board)
        return (nextMove.piece.getLoc(),nextMove.endPos)

    def nextMoveInternal(self,board):
        pieces = board.whitePieces if self.isWhite else board.blackPieces

        bestMove = None

        possibleMoves = []
        for piece in pieces:
            for move in piece.getValidMoves(board):
                possibleMoves.append(move)
        
        #print("\033[31m",possibleMoves,"\033[0m")

        for piece in pieces:
            moves = piece.getValidMoves(board)
            for move in moves:
                newBoard = copy.deepcopy(board)
                newBoard.movePiece(newBoard.getPiece(piece.getLoc()),move)

                # Returns the best move assuming the opponent picks the move that minimizes our benefit
                # If this comes back as None, the opponent has no valid moves (checkmate)
                calcMoveScoreRecersive = self.nextMoveRec(newBoard)
    
                newMove = PossibleMove(board,piece,move,calcMoveScoreRecersive.score if calcMoveScoreRecersive != None else 10000000)

                if calcMoveScoreRecersive == None:
                    print(newMove)

                if bestMove == None:
                    bestMove = newMove
                elif (bestMove != None and bestMove.score < newMove.score):
                    bestMove = newMove
        
        return bestMove
    
    def nextMoveRec(self,board,recursionLayer = 0):

        # Loop through all possible enemy moves and find the worst case scenario 
        enemyPieces = board.whitePieces if not self.isWhite else board.blackPieces

        worstMove = None

        for enemyPiece in enemyPieces:
            enemyMoves = enemyPiece.getValidMoves(board)
            for enemyMove in enemyMoves:
                enemyBoard = copy.deepcopy(board)
                enemyBoard.movePiece(enemyBoard.getPiece(enemyPiece.getLoc()),enemyMove)

                # For every move the enemy can make, find all the moves the bot can make and pick the best
                pieces = enemyBoard.whitePieces if self.isWhite else enemyBoard.blackPieces

                bestMove = None
                for piece in pieces:
                    moves = piece.getValidMoves(enemyBoard)
                    for move in moves:
                        newBoard = copy.deepcopy(enemyBoard)
                        if self.SHOW_THINKING:
                            print("\033[36m",newBoard, "\033[0m")
                            print("\033[36m ^^^^ ",piece, piece.getLoc(), piece.isAlive(), " ^^^^\033[0m")

                        newBoard.movePiece(newBoard.getPiece(piece.getLoc()),move)
                        
                        if recursionLayer < 0:
                            moveScore = self.nextMoveRec(newBoard,recursionLayer+1)
                        else:
                            moveScore = self.calcScore(newBoard, self.isWhite)

                        newMove = PossibleMove(enemyBoard,piece,move,moveScore)

                        if bestMove == None:
                            bestMove = newMove
                        elif (bestMove != None and bestMove.score < newMove.score):
                            bestMove = newMove

                newEnemyMove = PossibleMove(board,enemyPiece,enemyMove,bestMove.score if bestMove != None else -100000)

                if worstMove == None:
                    worstMove = newEnemyMove
                elif (worstMove != None and worstMove.score > newEnemyMove.score):
                    worstMove = newEnemyMove

        return worstMove



class PossibleMove:
    def __init__(self,board,piece,endPos,score):
        self.board = board
        self.piece = piece
        self.endPos = endPos
        self.score = score

        self.childList = []

    def __str__(self):
        return f"Board not shown ; Piece: {self.piece} ; endPos: {self.endPos} ; score: {self.score}"


