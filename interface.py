from board import *
import errors
import numpy as np
import numpy.typing as npt

colorDict = {-1: "Black", 1: "White"}
board = Board(customStart=['d2d4', 'd7d5', 'e2e4', 'd5e4', 'f2f4']) # ep test
# board = Board(customStart=['d2d4', 'e7e5', 'b1c3', 'g8f6', 'c1e3', 'f8d6', 'd1d2']) # castling test
# board = Board()


def clearScreen():
    # print("\033[H\033[J")
    # TODO: find way to actually clear screen
    pass


def renderBoard():
    clearScreen()
    board.printBoard()
    if len(board.checkMoveDict) != 0:
        print("\033[0;31;1mYou are in check!")
    print(f"\033[0;1m{colorDict[board.turnColor]}'s Turn:")
    invalidChoice = True
    startCoord = None
    endCoord = None
    promotionType = None
    cancelOptions = ["x", "cancel", "none", "no", "back"]
    while invalidChoice:
        validMoveList = board.coordListToAlgebra(board.pieceCanMoveList())
        if not validMoveList:
            raise errors.GameOver(board.stalemateWinnerMult * board.turnColor)
        elif board.halfMoveNum == 100 or board.nRepetitions(3):
            raise errors.GameOver(0)
        elif board.variantGameWinCondition() is not None:
            raise errors.GameOver(board.variantGameWinCondition())
        invalidStart = True
        while invalidStart:
            startAlg = input("\033[0mWhich piece would you like to move? (type ? for move options)\n")
            try:
                if startAlg == "?":
                    print(str(validMoveList))
                elif startAlg[-1] == "?":
                    startCoord = board.algebraToCoordinates(startAlg[:-1])
                    if board.pieceCanMove(startCoord):
                        print(str(board.coordListToAlgebra(board.validMoveOptions(startCoord))))
                    else:
                        raise errors.PieceCantMove
                else:
                    startCoord = board.algebraToCoordinates(startAlg)
                    if board.pieceCanMove(startCoord):
                        invalidStart = False
                    else:
                        raise errors.PieceCantMove
            except Exception as e:
                print(e)
        invalidEnd = True
        while invalidEnd:
            endAlg = input(
                "\033[0mWhich square would you like to move the piece to? (type ? for move options or x to cancel)\n").lower()
            # try:
            if endAlg == "?":
                print(str(board.coordListToAlgebra(board.validMoveOptions(startCoord))))
            elif endAlg in cancelOptions:
                invalidEnd = False
            else:
                endCoord = board.algebraToCoordinates(endAlg)
                if board.moveIsValid(startCoord, endCoord):
                    if endCoord[0] == board.nthRowForColor(0, board.turnColor * -1) and board.typeAt(
                            startCoord) == 'p':
                        invalidPromotion = True
                        while invalidPromotion:
                            promotion = input(
                                "\033[0mThis move will promote a pawn. Which type of piece would you like to promote it to? (type x to cancel)\n").lower()
                            try:
                                if promotion in cancelOptions:
                                    invalidPromotion = False
                                    invalidEnd = False
                                else:
                                    promotionType = board.promotionNameToType(
                                        promotion) if promotion in board.promotionTypes + board.promotionNames else None
                                    if promotionType is not None:
                                        invalidPromotion = False
                                        invalidEnd = False
                                        invalidChoice = False
                                    else:
                                        raise errors.InvalidSyntax
                            except Exception as e:
                                print(e)
                    else:
                        invalidEnd = False
                        invalidChoice = False
                else:
                    raise errors.InvalidMoveGeneric
            # except Exception as e:
            #     print(e)
    board.updateMoves(startCoord, endCoord, promotionType) if promotionType else board.updateMoves(startCoord, endCoord)


gameOver = False
while not gameOver:
    try:
        renderBoard()
    except errors.GameOver as e:
        print(e)
        gameOver = True
