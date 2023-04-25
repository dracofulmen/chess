from board import *
import errors
import numpy as np
import numpy.typing as npt

colorDict = {-1: "Black", 1: "White"}
# board = Board(customStart=['D2D4', 'D7D5', 'E2E4', 'D5E4', 'F2F4', 'E4F3']) # ep test
# board = Board(customPieces=['ra1w', 'ke1w', 'rh1w', 'qe7b', 'ra8b', 'ke8b', 'rh8b']) # check test
board = Board()


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
    promotionList = ['r', 'b', 'q', 'n', 'rook', 'bishop', 'queen', 'knight']
    cancelOptions = ["x", "cancel", "none", "no", "back"]
    while invalidChoice:
        validMoveList = board.coordListToAlgebra(board.pieceCanMoveList())
        if not validMoveList or board.drawTurn == 100:
            raise errors.GameOver(0)
        invalidStart = True
        while invalidStart:
            startAlg = input("\033[0mWhich piece would you like to move? (type ? for move options)\n")
            try:
                if startAlg == "?":
                    print(str(validMoveList))
                elif len(startAlg) == 2 or len(startAlg) == 3:
                    startCoord = board.algebraToCoordinates(startAlg[0:2])
                    if board.pieceCanMove(startCoord):
                        match len(startAlg):
                            case 3:
                                if startAlg[2] == "?":
                                    print(str(board.coordListToAlgebra(board.validMoveOptions(startCoord))))
                                else:
                                    raise errors.InvalidSyntax
                            case 2:
                                invalidStart = False
                    else:
                        raise errors.PieceCantMove
                else:
                    raise errors.InvalidSyntax
            except Exception as e:
                print(e)
        invalidEnd = True
        while invalidEnd:
            endAlg = input(
                "\033[0mWhich square would you like to move the piece to? (type ? for move options or x to cancel)\n").lower()
            try:
                if endAlg == "?":
                    print(str(board.coordListToAlgebra(board.validMoveOptions(startCoord))))
                elif endAlg in cancelOptions:
                    invalidEnd = False
                elif len(endAlg) == 2:
                    endCoord = board.algebraToCoordinates(endAlg[0:2])
                    if board.moveIsValid(startCoord, endCoord):
                        if endCoord[0] == 3.5 + 3.5 * board.turnColor and board.typeAt(startCoord) == 'p':
                            invalidPromotion = True
                            while invalidPromotion:
                                promotion = input(
                                    "\033[0mThis move will promote a pawn. Which type of piece would you like to promote it to? (type x to cancel)\n").lower()
                                try:
                                    if promotion in cancelOptions:
                                        invalidPromotion = False
                                        invalidEnd = False
                                    elif promotion in promotionList:
                                        promotionType = promotion[0]
                                        if promotionType == 'k':
                                            promotionType = 'n'
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
                else:
                    raise errors.InvalidSyntax
            except Exception as e:
                print(e)
    if promotionType:
        board.updateMoves(startCoord, endCoord, promotionType)
    else:
        board.updateMoves(startCoord, endCoord)


gameOver = False
while not gameOver:
    try:
        renderBoard()
    except errors.GameOver as e:
        print(e)
        gameOver = True
