from typing import Any, Callable, Optional

from piece import Piece
from piece import King
import errors
import numpy as np
import numpy.typing as npt

"""     
    TODO: add draws
        stalemate: no legal moves but not in check (DONE)
        dead position: neither player can checkmate the other by any legal series of moves (how to do with pawns?) (DONE for insufficient material but not pawns) 
        threefold repetition: (oh god no. i am not keeping track of every single board layout in the whole game.)
        fifty-move rule: fifty moves pass with no captures or pawn movements (DONE)
    
    all edge cases appear to work
    
    notations to implement:
        FEN for custom board https://www.chess.com/terms/fen-chess
    
    chess variants to add (use inheritance?):
        giveaway https://www.chess.com/terms/giveaway-chess
        atomic https://www.chess.com/terms/atomic-chess
        960 https://www.chess.com/terms/chess960
        3-check https://www.chess.com/terms/3-check-chess
        crazyhouse? (new UI elements) https://www.chess.com/terms/crazyhouse-chess
        duck? (new piece) https://www.chess.com/terms/duck-chess
        gothic? (new piece, bigger board) https://www.chess.com/terms/gothic-chess
        horde? https://www.chess.com/terms/horde-chess
        no castling https://www.chess.com/terms/no-castling-chess
        4-player? https://www.chess.com/terms/4-player-chess 
        torpedo https://www.chess.com/terms/torpedo-chess
        xxl? (new piece, bigger board) https://www.chess.com/terms/xxl-chess

"""


# TODO: big things: rewrite without numpy

class Board:
    def __init__(self, customPieces: list[str] = None,
                 customStart: list[str] = None, castleChecks: dict[[bool]] = None,
                 epCoord: npt.NDArray[int] | None = None, turnColor: int = 1):
        """
        initializes the board
        :param customPieces: custom starting pieces; format is type algebra color
        :param customStart: list of starting moves; will default to none
        :param castleChecks: custom starting values for whether kings and rooks have moved
        :param epCoord: en passant position when starting with a custom board
        :param turnColor: turn to move (1=white, -1=black)
        """
        if customPieces is not None:
            self.board = np.array(
                [np.fromiter((Piece(None, 0, moveList=[], blockList=[], captureList=[]) for j in range(8)), dtype=Piece)
                 for i in range(8)])
            colorDict = {'w': 1, 'b': -1}
            for pieceStr in customPieces:
                self.board[tuple(algebraToCoordinates(pieceStr[1:3]))] = Piece(pieceStr[0], colorDict[pieceStr[3]])
        else:
            endRow = np.array(['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'])
            pawnRow = np.fromiter(('p' for _ in range(8)), dtype=np.dtype('U1'))
            emptyRow = np.fromiter((None for _ in range(8)), dtype=type(None))
            colorCol = np.array([1, 1, 0, 0, 0, 0, -1, -1])
            typeBoard = np.array([endRow, pawnRow, emptyRow, emptyRow, emptyRow, emptyRow, pawnRow, endRow])
            self.board = np.array(
                [np.fromiter(
                    (Piece(typeBoard[i, j], colorCol[i], moveList=[], blockList=[], captureList=[]) for j in range(8)),
                    dtype=Piece) for i in range(8)])
        if castleChecks is None:
            self.castleChecks = {-1: [True for _ in range(3)], 1: [True for _ in range(3)]}
        else:
            self.castleChecks = castleChecks
        self.singleSquareVectorDict = {
            'k': np.array([[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]),
            'n': np.array([[2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2], [1, -2], [2, -1]]), 'q': None,
            'b': None, 'r': None, 'p': None}
        self.mutliSquareVectorDict = {'k': None, 'n': None, 'q': np.array(
            [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]),
                                      'b': np.array([[1, 1], [-1, 1], [-1, -1], [1, -1]]),
                                      'r': np.array([[1, 0], [0, 1], [-1, 0], [0, -1]]), 'p': None}
        self.pList = [np.array((0, -1)), np.array((0, 1))]
        self.kingDict = {}
        self.checkMoveDict = {}
        self.epCoord = epCoord
        self.epList = []
        self.turnColor = turnColor
        self.drawTurn = 0
        self.initMoves()
        if customPieces is not None:
            if self.inCheck(self.kingDict[self.turnColor].position, self.turnColor):
                self.kingDict[self.turnColor].inCheck = True
                self.enterCheckMode(self.turnColor)
        self.algList = []
        if customStart is not None:
            for move in customStart:
                startAlg = move[0:2]
                endAlg = move[2:4]
                startCoord = algebraToCoordinates(startAlg)
                endCoord = algebraToCoordinates(endAlg)
                if len(move) == 5:
                    promo = move[4]
                else:
                    promo = None
                if self.moveIsValid(startCoord, endCoord):
                    self.updateMoves(startCoord, endCoord, promotionType=promo)

    def __str__(self) -> str:
        """
        converts to string
        :return:
        """
        retStr = "\033[0m     A   B   C   D   E   F   G   H  "
        retStr += "\n\033[0m   ┌───┬───┬───┬───┬───┬───┬───┬───┐"
        for row in range(15, 0, -1):
            match row % 2:
                case 1:
                    retStr += "\n " + str(int((row + 1) / 2)) + " "
                    for col in range(8):
                        retStr += "\033[0m│\033[0m " + self.charAt((int((row - 1) / 2), col)) + " "
                    retStr += "\033[0m│ " + str(int((row + 1) / 2)) + " "
                case 0:
                    retStr += "\n\033[0m   ├───┼───┼───┼───┼───┼───┼───┼───┤"
        retStr += "\n\033[0m   └───┴───┴───┴───┴───┴───┴───┴───┘"
        retStr += "\n\033[0m     A   B   C   D   E   F   G   H  "
        return retStr

    def printBoard(self) -> None:
        """
        prints the string version of the board
        :return:
        """
        print(str(self))

    def pieceAt(self, coord: npt.NDArray[int] | tuple) -> Piece | None:
        """
        returns the piece object at a given set of coordinates
        :param coord: coordinates of the returned piece object
        :return: piece object at the given set of coordinates
        """
        return self.board[tuple(coord)]

    def typeAt(self, coord: npt.NDArray[int] | tuple) -> str | None:
        """
        returns the type of the piece at a given set of coordinates (p=pawn, r=rook, n=knight, b=bishop, k=king, q=queen)
        :param coord: coordinates of the piece to return the type of
        :return: type of the piece at the given set of coordinates
        """
        return self.board[tuple(coord)].pieceType

    def colorAt(self, coord: npt.NDArray[int] | tuple) -> int:
        """
        returns the color of the piece at a given set of coordinates (1=white, -1=black, 0=none)
        :param coord: coordinates of the piece to return the color of
        :return: color of the piece at the given set of coordinates
        """
        return self.board[tuple(coord)].color

    def charAt(self, coord: npt.NDArray[int] | tuple) -> str:
        """
        returns the character of the piece at a given set of coordinates
        :param coord: coordinates of the piece to return the color of
        :return: character of the piece at the given set of coordinates
        """
        return self.board[tuple(coord)].char()

    def movesAt(self, coord: npt.NDArray[int] | tuple) -> list[npt.NDArray[int]]:
        """
        returns the moveList of the piece at a given set of coordinates
        :param coord: coordinates of the piece to return the moveList of
        :return: moveList of the piece at the given set of coordinates
        """
        return self.board[tuple(coord)].moveList

    def canMoveTo(self, coord: npt.NDArray[int] | tuple, move: npt.NDArray[int] | tuple) -> bool:
        """
        checks if a piece at a given set of coordinates can move to another given set of coordinates and returns a bool
        :param coord: coordinates of the initial set of coordinates of the piece
        :param move: set of coordinates to check if the piece can move to
        :return: bool
        """
        if arrayInList(move, self.board[tuple(coord)].moveList):
            return True
        else:
            return False

    def canMoveToBools(self, coord: npt.NDArray[int] | tuple, moves: list[npt.NDArray[int]]) -> list[bool]:
        """
        checks if a piece at a given set of coordinates can move to a given list of sets of coordinates and returns a list of bools
        :param coord: coordinates of the initial set of coordinates of the piece
        :param moves: list of sets of coordinates to check if the piece can move to
        :return: bool
        """
        retList = []
        for move in moves:
            if arrayInList(move, self.board[tuple(coord)].moveList):
                retList.append(True)
            else:
                retList.append(False)
        return retList

    def canMoveList(self, coord: npt.NDArray[int] | tuple) -> list[npt.NDArray[int]]:
        """
        returns a list of the sets of coordinates of all pieces that can move to a given set of coordinates
        :param coord: coordinates to check if pieces can move to
        :return: list of the sets of coordinates of all pieces that can move to the given set of coordinates
        """
        squareList = []
        for i in range(8):
            for j in range(8):
                if arrayInList(coord, self.board[(j, i)].moveList):
                    squareList.append(np.array((j, i)))
        return squareList

    def addMoveAt(self, coord: npt.NDArray[int] | tuple, move: npt.NDArray[int]) -> None:
        """
        adds a given set of coordinates to the moveList of the piece at another given set of coordinates
        :param coord: coordinates of the piece whose moveList will be added to
        :param move: set of coordinates to add to the moveList of the piece at [y,x]
        :return: None
        """
        self.board[tuple(coord)].moveList.append(move)

    def addMovesAt(self, coord: npt.NDArray[int] | tuple, moves: list[npt.NDArray[int]]) -> None:
        """
        adds a given list of sets of coordinates to the moveList of the piece at another given set of coordinates
        :param coord: coordinates of the piece whose moveList will be added to
        :param moves: list of sets of coordinates to add to the moveList of the piece at [y,x]
        :return: None
        """
        for move in moves:
            self.board[tuple(coord)].moveList.append(move)

    def removeMoveAt(self, coord: npt.NDArray[int] | tuple, move: npt.NDArray[int]) -> None:
        """
        removes a given set of coordinates from the moveList of the piece at another given set of coordinates
        :param coord: coordinates of the piece whose moveList will be removed from
        :param move: set of coordinates to remove from the moveList of the piece at [y,x]
        :return: None
        """
        removeArray(move, self.board[tuple(coord)].moveList)

    def removeMovesAt(self, coord: npt.NDArray[int] | tuple, moves: list[npt.NDArray[int]]) -> None:
        """
        removes a given list of sets of coordinates from the moveList of the piece at another given set of coordinates
        :param coord: coordinates of the piece whose moveList will be removed from
        :param moves: list of sets of coordinates to remove from the moveList of the piece at [y,x]
        :return: None
        """
        for move in moves:
            removeArray(move, self.board[tuple(coord)].moveList)

    def clearMovesAt(self, coord: npt.NDArray[int] | tuple) -> None:
        """
        clears the moveList at a given set of coordinates
        :param coord: coordinates of the piece whose moveList will be cleared
        :return: None
        """
        self.board[tuple(coord)].moveList.clear()

    def blocksAt(self, coord: npt.NDArray[int] | tuple) -> list[npt.NDArray[int]]:
        """
        returns the blockList of the piece at a given set of coordinates
        :param coord: coordinates of the piece to return the blockList of
        :return: blockList of the piece at the given set of coordinates
        """
        return self.board[tuple(coord)].blockList

    def blockedAt(self, coord: npt.NDArray[int] | tuple, block: npt.NDArray[int]) -> bool:
        """
        checks if a piece at a given set of coordinates is blocked at another given set of coordinates and returns a bool
        :param coord: coordinates of the initial set of coordinates of the piece
        :param block: set of coordinates to check if the piece is blocked at
        :return: bool
        """
        if arrayInList(block, self.board[tuple(coord)].blockList):
            return True
        else:
            return False

    def blockedAtBools(self, coord: npt.NDArray[int] | tuple, blocks: list[npt.NDArray[int]]) -> list[bool]:
        """
        checks if a piece at a given set of coordinates is blocked at a given list of sets of coordinates and returns a list of bools
        :param coord: coordinates of the initial set of coordinates of the piece
        :param blocks: list of sets of coordinates to check if the piece is blocked at
        :return: bool
        """
        retList = []
        for block in blocks:
            if arrayInList(block, self.board[tuple(coord)].blockList):
                retList.append(True)
            else:
                retList.append(False)
        return retList

    def blockedAtList(self, coord: npt.NDArray[int] | tuple) -> list[npt.NDArray[int]]:
        """
        returns a list of the sets of coordinates of all pieces that are blocked at a given set of coordinates
        :param coord: coordinates to check if pieces are blocked at
        :return: list of the sets of coordinates of all pieces that are blocked at the given set of coordinates
        """
        squareList = []
        for i in range(8):
            for j in range(8):
                if arrayInList(coord, self.board[(j, i)].blockList):
                    squareList.append(np.array((j, i)))
        return squareList

    def addBlockAt(self, coord: npt.NDArray[int] | tuple, block: npt.NDArray[int]) -> None:
        """
        adds a given set of coordinates to the blockList of the piece at another given set of coordinates
        :param coord: coordinates of the piece whose blockList will be added to
        :param block: set of coordinates to add to the blockList of the piece at [y,x]
        :return: None
        """
        self.board[tuple(coord)].blockList.append(block)

    def addBlocksAt(self, coord: npt.NDArray[int] | tuple, blocks: list[npt.NDArray[int]]) -> None:
        """
        adds a given list of sets of coordinates to the blockList of the piece at another given set of coordinates
        :param coord: coordinates of the piece whose blockList will be added to
        :param blocks: list of sets of coordinates to add to the blockList of the piece at [y,x]
        :return: None
        """
        for block in blocks:
            self.board[tuple(coord)].blockList.append(block)

    def removeBlockAt(self, coord: npt.NDArray[int] | tuple, block: npt.NDArray[int]) -> None:
        """
        removes a given set of coordinates from the blockList of the piece at another given set of coordinates
        :param coord: coordinates of the piece whose blockList will be removed from
        :param block: set of coordinates to remove from the blockList of the piece at [y,x]
        :return: None
        """
        removeArray(block, self.board[tuple(coord)].blockList)

    def removeBlocksAt(self, coord: npt.NDArray[int] | tuple, blocks: list[npt.NDArray[int]]) -> None:
        """
        removes a given list of sets of coordinates from the blockList of the piece at another given set of coordinates
        :param coord: coordinates of the piece whose blockList will be removed from
        :param blocks: list of sets of coordinates to remove from the blockList of the piece at [y,x]
        :return: None
        """
        for block in blocks:
            removeArray(block, self.board[tuple(coord)].blockList)

    def clearBlocksAt(self, coord: npt.NDArray[int] | tuple) -> None:
        """
        clears the blockList at a given set of coordinates
        :param coord: coordinates of the piece whose blockList will be cleared
        :return: None
        """
        self.board[tuple(coord)].blockList.clear()

    def capturesAt(self, coord: npt.NDArray[int] | tuple) -> list[npt.NDArray[int]]:
        """
        returns the captureList of the piece at a given set of coordinates
        :param coord: coordinates of the piece to return the captureList of
        :return: captureList of the piece at the given set of coordinates
        """
        return self.board[tuple(coord)].captureList

    def capturedAt(self, coord: npt.NDArray[int] | tuple, capture: npt.NDArray[int]) -> bool:
        """
        checks if a piece at a given set of coordinates has a capture at another given set of coordinates and returns a bool
        :param coord: coordinates of the initial set of coordinates of the piece
        :param capture: set of coordinates to check if the piece has a capture
        :return: bool
        """
        if arrayInList(capture, self.board[tuple(coord)].captureList):
            return True
        else:
            return False

    def capturedAtBools(self, coord: npt.NDArray[int] | tuple, captures: list[npt.NDArray[int]]) -> list[bool]:
        """
        checks if a piece at a given set of coordinates has a capture at a given list of sets of coordinates and returns a list of bools
        :param coord: coordinates of the initial set of coordinates of the piece
        :param captures: list of sets of coordinates to check if the piece has a capture
        :return: bool
        """
        retList = []
        for capture in captures:
            if arrayInList(capture, self.board[tuple(coord)].captureList):
                retList.append(True)
            else:
                retList.append(False)
        return retList

    def capturedList(self, coord: npt.NDArray[int] | tuple) -> list[npt.NDArray[int]]:
        """
        returns a list of the sets of coordinates of all pieces that have a capture at a given set of coordinates
        :param coord: coordinates to check if pieces can capture
        :return: list of the sets of coordinates of all pieces that have a capture at the given set of coordinates
        """
        squareList = []
        for i in range(8):
            for j in range(8):
                if arrayInList(coord, self.board[(j, i)].captureList):
                    squareList.append(np.array((j, i)))
        return squareList

    def addCaptureAt(self, coord: npt.NDArray[int] | tuple, capture: npt.NDArray[int]) -> None:
        """
        adds a given set of coordinates to the captureList of the piece at another given set of coordinates
        :param coord: coordinates of the piece whose captureList will be added to
        :param capture: set of coordinates to add to the captureList of the piece at [y,x]
        :return: None
        """
        self.board[tuple(coord)].captureList.append(capture)

    def addCapturesAt(self, coord: npt.NDArray[int] | tuple, captures: list[npt.NDArray[int]]) -> None:
        """
        adds a given list of sets of coordinates to the captureList of the piece at another given set of coordinates
        :param coord: coordinates of the piece whose captureList will be added to
        :param captures: list of sets of coordinates to add to the captureList of the piece at [y,x]
        :return: None
        """
        for capture in captures:
            self.board[tuple(coord)].captureList.append(capture)

    def removeCaptureAt(self, coord: npt.NDArray[int] | tuple, capture: npt.NDArray[int]) -> None:
        """
        removes a given set of coordinates from the captureList of the piece at another given set of coordinates
        :param coord: coordinates of the piece whose captureList will be removed from
        :param capture: set of coordinates to remove from the captureList of the piece at [y,x]
        :return: None
        """
        removeArray(capture, self.board[tuple(coord)].captureList)

    def removeCapturesAt(self, coord: npt.NDArray[int] | tuple, captures: list[npt.NDArray[int]]) -> None:
        """
        removes a given list of sets of coordinates from the captureList of the piece at another given set of coordinates
        :param coord: coordinates of the piece whose captureList will be removed from
        :param captures: list of sets of coordinates to remove from the captureList of the piece at [y,x]
        :return: None
        """
        for capture in captures:
            removeArray(capture, self.board[tuple(coord)].captureList)

    def clearCapturesAt(self, coord: npt.NDArray[int] | tuple) -> None:
        """
        clears the captureList at a given set of coordinates
        :param coord: coordinates of the piece whose captureList will be cleared
        :return: None
        """
        self.board[tuple(coord)].captureList.clear()

    def setEP(self, ep: npt.NDArray[int] | tuple, color: int) -> None:
        """
        sets the coordinates of the square that must be gone to in order to make an en passant capture
        :param ep: coordinates of the square that must be gone to in order to make an en passant capture
        :param color: color of the piece that can be captured in en passant
        :return:
        """
        self.clearEP()
        self.epCoord = ep
        for v in self.pList:
            if (0 <= ep[1] + v[1] <= 7) and self.colorAt((ep[0] + color, ep[1] + v[1])) * color == -1 and self.typeAt(
                    (ep[0] + color, ep[1] + v[1])) == 'p' and self.colorAt(ep) == 0:
                self.addCaptureAt((ep[0] + color, ep[1] + v[1]), ep)
                self.epList.append(np.array((ep[0] + color, ep[1] + v[1])))

    def clearEP(self) -> None:
        """
        clears the en passant coordinates
        :return:
        """
        if self.epCoord is not None:
            epList = self.epList
            self.epList.clear()
            for coord in epList:
                self.removeCaptureAt(coord, self.epCoord)
            self.epCoord = None

    def usesEP(self, startCoord: npt.NDArray[int] | tuple, endCoord: npt.NDArray[int] | tuple) -> bool:
        """
        checks if a move from one square to another uses en passant
        :param startCoord: start coordinates of the move
        :param endCoord: end coordinates of the move
        :return:
        """
        if self.epCoord is not None and arrayInList(startCoord, self.epList) and np.array_equal(self.epCoord, endCoord):
            return True
        else:
            return False

    def iterateUntilNextOccupiedSquare(self, startCoord: npt.NDArray[int], dirVector: npt.NDArray[int],
                                       squareFunc: Optional[Callable], *args, skipCoord: npt.NDArray[int] = None,
                                       stopCoord: npt.NDArray[int] = None, **kwargs) -> npt.NDArray[int] | None:
        """
        iterates over the board from a starting square in a direction until it hits an occupied square, calling a function on all squares in the middle, and returns the occupied square
        :param startCoord: square to start from (exclusive)
        :param dirVector: vector to iterate with
        :param squareFunc: function to call on squares in the middle
        :param skipCoord: optional coordinate to ignore color at
        :param stopCoord: optional coordinate to stop at if reached
        :return:
        """
        curPos = startCoord + dirVector
        while (0 <= curPos[0] <= 7) and (0 <= curPos[1] <= 7) and (
                not self.colorAt(curPos) or (skipCoord is not None and np.array_equal(curPos, skipCoord))) and (
                stopCoord is None or not np.array_equal(curPos, stopCoord)):
            if squareFunc is not None:
                squareFunc(*args, curPos.copy(), **kwargs)
            curPos += dirVector
        else:
            if (0 <= curPos[0] <= 7) and (0 <= curPos[1] <= 7):
                return curPos
            else:
                return None

    def generateListsAt(self, coord: npt.NDArray[int] | tuple) -> None:
        """
        generates the moveList, blockList, and captureList at a given set of coordinates
        :param coord: coordinates of the piece whose lists will be generated
        :return: None
        """
        moveList = []
        blockList = []
        captureList = []
        curType = self.typeAt(coord)
        color = self.colorAt(coord)
        y: int = coord[0]
        x: int = coord[1]
        if type(coord) == tuple:
            arrayCoord = np.array(coord)
        else:
            arrayCoord = coord
        if curType == 'p':
            if not self.colorAt((y + color, x)):
                moveList.append(np.array([y + color, x]))
                if y == 3.5 - 2.5 * color:
                    if self.colorAt((y + 2 * color, x)):
                        blockList.append(np.array([y + 2 * color, x]))
                    else:
                        moveList.append(np.array([y + 2 * color, x]))
            else:
                blockList.append(np.array([y + color, x]))
            for i in [-1, 1]:
                if (0 <= x + i <= 7) and self.colorAt((y + color, x + i)) * color == -1:
                    captureList.append(np.array([y + color, x + i]))
        elif curType is not None:
            if curType == 'k':
                inCheck = self.inCheck(coord, color)
                self.kingDict[self.colorAt(coord)] = King(inCheck, arrayCoord)
            if self.singleSquareVectorDict[curType] is not None:
                for v in self.singleSquareVectorDict[curType]:
                    curPos = arrayCoord + v
                    if (0 <= curPos[0] <= 7) and (0 <= curPos[1] <= 7):
                        match color * self.colorAt(curPos):
                            case 1:
                                blockList.append(curPos)
                            case 0:
                                moveList.append(curPos)
                            case -1:
                                captureList.append(curPos)
            if self.mutliSquareVectorDict[curType] is not None:
                for v in self.mutliSquareVectorDict[curType]:
                    endPos = self.iterateUntilNextOccupiedSquare(arrayCoord, v, moveList.append)
                    if endPos is not None:
                        match self.colorAt(endPos) * color:
                            case 1:
                                blockList.append(endPos)
                            case -1:
                                captureList.append(endPos)
        self.addMovesAt(coord, moveList)
        self.addBlocksAt(coord, blockList)
        self.addCapturesAt(coord, captureList)

    def initMoves(self) -> None:
        """
        initializes the moveLists, blockLists, and captureLists
        :return:
        """
        for y in range(8):
            for x in range(8):
                self.generateListsAt((y, x))
        if self.epCoord is not None:
            self.setEP(self.epCoord, self.turnColor * -1)

    def addPieceAt(self, coord: npt.NDArray[int], pieceType: str, color: int) -> None:
        """
        adds a piece to a given set of coordinates and updates moveLists, blockLists, and captureLists
        :param coord: coordinates to add the piece
        :param pieceType: type of the piece to add
        :param color: color of the piece to add
        :return:
        """
        oldColor = self.colorAt(coord)
        self.board[tuple(coord)] = Piece(pieceType, color)
        match oldColor:
            case 0:
                updateList = self.canMoveList(coord)
                for square in updateList:
                    curType = self.typeAt(square)
                    curColor = self.colorAt(square)
                    dirVec = vector(square, coord)
                    match curType:
                        case 'p':
                            self.removeMoveAt(square, coord)
                            self.addBlockAt(square, coord)
                            curPos = dirVec[0] + coord
                            if self.canMoveTo(square, curPos):
                                self.removeMoveAt(square, curPos)
                        case 'r' | 'b' | 'q':
                            self.removeMoveAt(square, coord)
                            match curColor * color:
                                case 1:
                                    self.addBlockAt(square, coord)
                                case -1:
                                    self.addCaptureAt(square, coord)
                            endPos = self.iterateUntilNextOccupiedSquare(coord, dirVec[0], self.removeMoveAt, square)
                            if endPos is not None:
                                match self.colorAt(endPos) * color:
                                    case 1:
                                        self.removeBlockAt(square, endPos)
                                    case -1:
                                        self.removeCaptureAt(square, endPos)
                        case 'n' | 'k':
                            self.removeMoveAt(square, coord)
                            match curColor * color:
                                case 1:
                                    self.addBlockAt(square, coord)
                                case -1:
                                    self.addCaptureAt(square, coord)
            case -1 | 1:
                updateBlockList = self.blockedAtList(coord)
                updateCaptureList = self.capturedList(coord)
                for square in updateBlockList:
                    if self.typeAt(square) != 'p':
                        self.removeBlockAt(square, coord)
                        self.addCaptureAt(square, coord)
                for square in updateCaptureList:
                    self.removeCaptureAt(square, coord)
                    if self.typeAt(square) != 'p':
                        self.addBlockAt(square, coord)
        for i in [-1, 1]:
            pawnPos = (coord[0] + color, coord[1] + i)
            if 0 <= pawnPos[0] <= 7 and 0 <= pawnPos[1] + i <= 7 and self.colorAt(
                    pawnPos) * color == -1 and self.typeAt(pawnPos) == 'p':
                self.addCaptureAt(pawnPos, coord)
        self.generateListsAt(coord)
        if pieceType == 'k':
            self.kingDict[color].position = coord

    def removePieceAt(self, coord: npt.NDArray[int]) -> None:
        """
        removes a piece from a given set of coordinates and updates moveLists, blockLists, and captureLists (technically replaces it with an empty piece)
        :param coord: coordinates to remove the piece from
        :return:
        """
        color = self.colorAt(coord)
        updateList = self.blockedAtList(coord) + self.capturedList(coord)
        self.board[tuple(coord)] = Piece(None, 0)
        for square in updateList:
            curType = self.typeAt(square)
            curColor = self.colorAt(square)
            dirVec = vector(square, coord)
            match curType:
                case 'p':
                    if square[0] != coord[0]:
                        match square[1] - coord[1]:
                            case 0:
                                self.removeBlockAt(square, coord)
                                self.addMoveAt(square, coord)
                            case 1 | -1:
                                self.removeCaptureAt(square, coord)
                        if square[0] == 3.5 - 2.5 * color and coord[0] == 3.5 - 1.5 * color:
                            curPos = dirVec[0] + coord
                            match color * self.colorAt(curPos):
                                case 1 | -1:
                                    self.addBlockAt(square, curPos)
                                case 0:
                                    self.addMoveAt(square, curPos)
                case 'r' | 'b' | 'q':
                    self.addMoveAt(square, coord)
                    match curColor * color:
                        case 1:
                            self.removeBlockAt(square, coord)
                        case -1:
                            self.removeCaptureAt(square, coord)
                    endPos = self.iterateUntilNextOccupiedSquare(coord, dirVec[0], self.addMoveAt, square)
                    if endPos is not None:
                        match self.colorAt(endPos) * color:
                            case 1:
                                self.addBlockAt(square, endPos)
                            case -1:
                                self.addCaptureAt(square, endPos)
                case 'n' | 'k':
                    self.addMoveAt(square, coord)
                    match curColor * color:
                        case 1:
                            self.removeBlockAt(square, coord)
                        case -1:
                            self.removeCaptureAt(square, coord)
        self.generateListsAt(coord)

    def threatenListAt(self, coord: npt.NDArray[int] | tuple, color: int) -> list[npt.NDArray[int]]:
        """
        returns a list of the coordinates of all pieces that threaten a space if it was occupied by a certain color
        :param coord: coordinates to check if threatened
        :param color: color of piece to check if threatened by
        :return: bool
        """
        threatenList = []
        squareList = self.canMoveList(coord) + self.blockedAtList(coord) + self.capturedList(coord)
        for square in squareList:
            if self.colorAt(square) * color == -1:
                threatenList.append(square)
        return threatenList

    def inCheck(self, coord: npt.NDArray[int] | tuple, color: int) -> bool:
        """
        returns a bool corresponding to whether a given set of coordinates is in check
        :param coord: coordinates to check if in check
        :param color: color of king to check if in check
        :return: bool
        """
        squareList = self.canMoveList(coord) + self.blockedAtList(coord) + self.capturedList(coord)
        for square in squareList:
            if self.colorAt(square) * color == -1:
                return True
        return False

    def exposesKing(self, startCoord: npt.NDArray[int], endCoord: npt.NDArray[int], kingCoord: npt.NDArray[int],
                    color: int) -> bool:
        """
        checks if moving a non-king piece from one place to another would expose that side's king and returns a bool
        :param startCoord: coordinates the piece starts at
        :param endCoord: coordinates the piece ends at
        :param kingCoord: coordinates of the king
        :param color: color moving pieces
        :return:
        """
        exposureList = self.blockedAtList(startCoord) + self.capturedList(startCoord)
        exposureList = [square for square in exposureList if self.colorAt(square) * color == -1]
        if self.usesEP(startCoord, endCoord):
            epCapCoord = np.array((startCoord[0], endCoord[1]))
            epExposureList = self.blockedAtList(epCapCoord) + self.capturedList(epCapCoord)
            epExposureList = [square for square in epExposureList if self.colorAt(square) * color == -1]
            epDoubleExposureList = [square for square in epExposureList + exposureList if
                                    square[0] == startCoord[0] and (
                                            self.typeAt(square) == 'r' or self.typeAt(square) == 'q')]
            for square in epDoubleExposureList:
                dirVec = vector(square, startCoord)
                startPos = np.array((startCoord[0], endCoord[1] + (
                        np.sign(dirVec[0][1]) * (endCoord[1] - startCoord[1]) * 0.5 - 0.5) * np.sign(dirVec[0][1])))
                endPos = self.iterateUntilNextOccupiedSquare(startPos, dirVec[0], None)
                if np.array_equal(endPos, kingCoord):
                    return True
            epExposureList = [square for square in epExposureList if not arrayInList(square, epDoubleExposureList)]
            for square in epExposureList:
                curType = self.typeAt(square)
                if curType == 'r' or curType == 'b' or curType == 'q':
                    dirVec = vector(square, epCapCoord)
                    endPos = self.iterateUntilNextOccupiedSquare(square, dirVec[0], None, skipCoord=epCapCoord,
                                                                 stopCoord=endCoord)
                    if np.array_equal(endPos, kingCoord):
                        return True
            exposureList = [square for square in exposureList if not arrayInList(square, epDoubleExposureList)]
        for square in exposureList:
            curType = self.typeAt(square)
            if curType == 'r' or curType == 'b' or curType == 'q':
                dirVec = vector(square, startCoord)
                endPos = self.iterateUntilNextOccupiedSquare(square, dirVec[0], None, skipCoord=startCoord,
                                                             stopCoord=endCoord)
                if np.array_equal(endPos, kingCoord):
                    return True
        threatenList = self.threatenListAt(kingCoord, color)
        if arrayInList(endCoord, threatenList):
            removeArray(endCoord, threatenList)
        if len(threatenList) == 0:
            return False
        else:
            for square in threatenList:
                curType = self.typeAt(square)
                if curType == 'r' or curType == 'b' or curType == 'q':
                    dirVec = vector(square, kingCoord)
                    endPos = self.iterateUntilNextOccupiedSquare(square, dirVec[0], None, stopCoord=endCoord)
                    if np.array_equal(endPos, kingCoord):
                        return True
                else:
                    return True
            return False

    def enterCheckMode(self, color: int) -> None:
        """
        enters check mode for the given color (restricts moves to those possible during check)
        :param color: color in check
        :return:
        """
        kingCoord = self.kingDict[color].position
        self.checkMoveDict.clear()
        for y in range(8):
            for x in range(8):
                if self.colorAt((y, x)) == color:
                    if self.typeAt((y, x)) == 'k':
                        optionList = []
                        blockList = self.blocksAt(kingCoord)
                        for v in self.singleSquareVectorDict['k']:
                            curPos = kingCoord + v
                            if (0 <= curPos[0] <= 7) and (0 <= curPos[1] <= 7) and not self.inCheck(curPos,
                                                                                                    color) and not arrayInList(
                                curPos, blockList):
                                optionList.append(curPos)
                        if len(optionList) != 0:
                            self.checkMoveDict[tuple(kingCoord)] = optionList
                    else:
                        coord = np.array((y, x))
                        moveList = self.movesAt((y, x)) + self.capturesAt((y, x))
                        optionList = []
                        for option in moveList:
                            if not self.exposesKing(coord, option, kingCoord, color):
                                optionList.append(option)
                        if len(optionList) != 0:
                            self.checkMoveDict[(y, x)] = optionList
        if len(self.checkMoveDict) == 0:
            raise errors.GameOver(color * -1)

    def pieceCanMove(self, coord: npt.NDArray[int]) -> bool:
        """
        checks if a given piece can move and returns a bool
        :param coord: coordinates of the piece to check if it can move
        :return:
        """
        color = self.colorAt(coord)
        if color != self.turnColor:
            raise errors.InvalidMoveWrongColor
        elif not (0 <= coord[0] <= 7) or not (0 <= coord[1] <= 7):
            raise errors.InvalidMoveOffBoard
        elif self.kingDict[color].inCheck:
            if tuple(coord) in self.checkMoveDict.keys():
                return True
            else:
                raise errors.InvalidMoveCheck
        optionList = self.validMoveOptions(coord)
        if optionList:
            return True
        else:
            raise errors.PieceCantMove

    def moveIsValid(self, startCoord: npt.NDArray[int], endCoord: npt.NDArray[int]) -> bool:
        """
        checks if a given move is valid and returns a bool
        :param startCoord: starting coordinates of the piece to check the move of
        :param endCoord: ending coordinates of the piece to check the move of
        :return:
        """
        pieceType = self.typeAt(startCoord)
        color = self.colorAt(startCoord)
        if color != self.turnColor:
            raise errors.InvalidMoveWrongColor
        elif not (0 <= startCoord[0] <= 7) or not (0 <= startCoord[1] <= 7) or not (0 <= endCoord[0] <= 7) or not (
                0 <= endCoord[1] <= 7):
            raise errors.InvalidMoveOffBoard
        elif self.colorAt(endCoord) * color == 1:
            raise errors.InvalidMoveBlocked
        elif self.kingDict[color].inCheck:
            if tuple(startCoord) in self.checkMoveDict.keys():
                if arrayInList(endCoord, self.checkMoveDict[tuple(startCoord)]):
                    return True
                else:
                    raise errors.InvalidMoveCheck
            else:
                raise errors.InvalidMoveCheck
        elif self.exposesKing(startCoord, endCoord, self.kingDict[color].position, color):
            raise errors.InvalidMoveIntoCheck
        elif pieceType == 'k':
            if abs(vector(startCoord, endCoord)[1]) == 2 and startCoord[1] == 4 and startCoord[
                0] == 3.5 - 3.5 * color and self.castleChecks[color][1]:  # castling
                row = int(3.5 - 3.5 * color)
                match endCoord[1]:
                    case 2:
                        if self.castleChecks[color][0] and self.typeAt((row, 0)) == 'r' and self.colorAt(
                                (row, 0)) == color and not self.typeAt((row, 3)) and not self.typeAt(
                            (row, 2)) and not self.typeAt((row, 1)) and not self.inCheck((row, 3),
                                                                                         color) and not self.inCheck(
                            (row, 2), color):
                            return True
                        else:
                            raise errors.InvalidMoveCastle
                    case 6:
                        if self.castleChecks[color][2] and self.typeAt((row, 7)) == 'r' and self.colorAt(
                                (row, 7)) == color and not self.typeAt((row, 5)) and not self.typeAt(
                            (row, 6)) and not self.inCheck((row, 5), color) and not self.inCheck((row, 6), color):
                            return True
                        else:
                            raise errors.InvalidMoveCastle
                    case _:
                        raise errors.InvalidMoveGeneric
            elif not self.inCheck(endCoord, color) and (
                    self.canMoveTo(startCoord, endCoord) or self.capturedAt(startCoord, endCoord)):
                return True
            else:
                raise errors.InvalidMoveGeneric
        elif pieceType == 'p' and self.usesEP(startCoord, endCoord):
            return True
        elif self.canMoveTo(startCoord, endCoord) or self.capturedAt(startCoord, endCoord):
            return True
        else:
            raise errors.InvalidMoveGeneric

    def validMoveOptions(self, coord: npt.NDArray[int]) -> list[npt.NDArray[int]]:
        """
        gives the list of all valid moves for a given set of coordinates
        :param coord: coordinates of the piece to move
        :return:
        """
        pieceType = self.typeAt(coord)
        color = self.colorAt(coord)
        if color == 0:
            return []
        optionList = self.movesAt(coord) + self.capturesAt(coord)
        optionList = [square for square in optionList if self.colorAt(square) * color != 1]
        retList = []
        for square in optionList:
            if self.kingDict[color].inCheck and tuple(coord) in self.checkMoveDict.keys() and arrayInList(square,
                                                                                                          self.checkMoveDict[
                                                                                                              tuple(
                                                                                                                  coord)]):
                retList.append(square)
            elif self.exposesKing(coord, square, self.kingDict[color].position, color):
                pass
            elif pieceType == 'k':
                if abs(vector(coord, square)[1]) == 2 and coord[1] == 4 and coord[0] == 3.5 - 3.5 * color and \
                        self.castleChecks[color][1]:  # castling
                    row = int(3.5 - 3.5 * color)
                    match square[1]:
                        case 2:
                            if self.castleChecks[color][0] and self.typeAt((row, 0)) == 'r' and self.colorAt(
                                    (row, 0)) == color and not self.typeAt((row, 3)) and not self.typeAt(
                                (row, 2)) and not self.typeAt((row, 1)) and not self.inCheck((row, 3),
                                                                                             color) and not self.inCheck(
                                (row, 2), color):
                                retList.append(square)
                        case 6:
                            if self.castleChecks[color][2] and self.typeAt((row, 7)) == 'r' and self.colorAt(
                                    (row, 7)) == color and not self.typeAt((row, 5)) and not self.typeAt(
                                (row, 6)) and not self.inCheck((row, 5), color) and not self.inCheck((row, 6),
                                                                                                     color):
                                retList.append(square)
                elif not self.inCheck(square, color) and (
                        self.canMoveTo(coord, square) or self.capturedAt(coord, square)):
                    retList.append(square)
            elif pieceType == 'p' and self.usesEP(coord, square):
                retList.append(square)
            elif self.canMoveTo(coord, square) or self.capturedAt(coord, square):
                retList.append(square)
        if retList:
            return retList
        else:
            return []

    def pieceCanMoveList(self) -> list[npt.NDArray[int]]:
        """
        gives the list of all pieces that can move
        :return:
        """
        pieceList = []
        if self.kingDict[self.turnColor].inCheck:
            return [np.array(coord) for coord in list(self.checkMoveDict.keys())]
        for y in range(8):
            for x in range(8):
                color = self.colorAt((y, x))
                if color == self.turnColor:
                    coord = np.array((y, x))
                    if self.validMoveOptions(coord):
                        pieceList.append(coord)
        return pieceList

    def positionIsDead(self) -> bool:
        """
        checks if the board is in a dead position
        :return:
        """
        nonKingCoord = None
        nonKingColor = 0
        nonKingType = None
        secondBishop = None
        for y in range(8):
            for x in range(8):
                curType = self.typeAt((y, x))
                curColor = self.colorAt((y, x))
                if curType is not None:
                    if not nonKingType and (curType == 'n' or curType == 'b'):
                        nonKingCoord = (y, x)
                        nonKingColor = curColor
                        nonKingType = curType
                    elif not secondBishop and nonKingType == 'b' and curType == 'b' and curColor * nonKingColor == -1 and (
                            y - x) % 2 == (nonKingCoord[0] - nonKingCoord[1]) % 2:
                        secondBishop = True
                    elif curType != 'k':
                        return False
        return True

    def updateMoves(self, startCoord: npt.NDArray[int], endCoord: npt.NDArray[int], promotionType: str = None) -> None:
        """
        moves a piece from one location to another and updates all lists
        :param startCoord: starting coordinates of the piece to move
        :param endCoord: ending coordinates of the piece to move
        :param promotionType: type of piece to promote a pawn moving to opponent's end row to (defaults to queen)
        :return:
        """
        pieceType = self.typeAt(startCoord)
        color = self.colorAt(startCoord)
        if pieceType == 'p' or color * self.colorAt(endCoord) == -1:
            self.drawTurn = 0
        else:
            self.drawTurn += 1
        if pieceType == 'k' and abs(endCoord[1] - startCoord[1]) == 2:
            self.castleChecks[color][1] = False
            if endCoord[1] == 2:
                self.castleChecks[color][0] = False
                rookStartCoord = np.array([startCoord[0], 0])
                rookEndCoord = np.array([startCoord[0], 3])
            else:
                self.castleChecks[color][2] = False
                rookStartCoord = np.array([startCoord[0], 7])
                rookEndCoord = np.array([startCoord[0], 5])
            self.removePieceAt(rookStartCoord)
            self.addPieceAt(rookEndCoord, 'r', color)
        elif pieceType == 'p' and self.usesEP(startCoord, endCoord):
            self.removePieceAt(
                np.array((self.epCoord[0] - color, self.epCoord[1])))
        elif (pieceType == 'k' or pieceType == 'r') and 3.5 - 3.5 * color:
            match startCoord[0]:
                case 0:
                    if self.castleChecks[color][0]:
                        self.castleChecks[color][0] = False
                case 4:
                    if self.castleChecks[color][1]:
                        self.castleChecks[color][1] = False
                case 7:
                    if self.castleChecks[color][2]:
                        self.castleChecks[color][2] = False
        self.removePieceAt(startCoord)
        if pieceType == 'p' and endCoord[0] == 3.5 + 3.5 * color:
            if promotionType:
                self.addPieceAt(endCoord, promotionType, color)
            else:
                self.addPieceAt(endCoord, 'q', color)
        else:
            self.addPieceAt(endCoord, pieceType, color)
        if pieceType == 'p' and startCoord[0] == 3.5 - 2.5 * color and endCoord[0] == 3.5 - 0.5 * color:
            self.setEP((endCoord[0] - color, endCoord[1]), color)
        else:
            self.clearEP()
        self.checkMoveDict.clear()
        for i in [-1, 1]:
            self.kingDict[i].inCheck = self.inCheck(self.kingDict[i].position, i)
            if self.kingDict[i].inCheck:
                self.enterCheckMode(i)
        self.turnColor *= -1
        self.algList.append(coordToAlgebra(startCoord) + coordToAlgebra(endCoord) + str(promotionType or ""))

    def printStatus(self, printMoves: bool = True, printBlocks: bool = True, printCaptures: bool = True):
        for y in range(8):
            for x in range(8):
                print(str(coordToAlgebra((y, x))) + ": " + str(self.typeAt((y, x))) + " " + str(self.colorAt((y, x))))
                if printMoves:
                    print("Moves: " + str(self.movesAt((y, x))))
                if printBlocks:
                    print("Blocks: " + str(self.blocksAt((y, x))))
                if printCaptures:
                    print("Captures: " + str(self.capturesAt((y, x))))


def algebraToCoordinates(algebra: str) -> npt.NDArray[int] | None:
    """
    converts algebraic notation into a set of coordinates
    :param algebra: algebraic notation to be converted into a set of coordinates (e.g. A1 -> [0,0], A8 -> [0,7], H8 -> [7,7])
    :return: set of coordinates
    """
    if len(algebra) != 2:
        return None
    else:
        row = int(algebra[1]) - 1
        col = ord(algebra[0].upper()) - 65
        if (0 <= row <= 7) and (0 <= col <= 7):
            retNP = np.array((row, col))
            return retNP
        else:
            raise errors.InvalidSyntax


def coordToAlgebra(coord: npt.NDArray[int] | tuple) -> str | None:
    """
    converts a set of coordinates into algebraic notation
    :param coord: set of coordinates to be converted into algebraic notation (e.g. [0,0] -> A1, [7,7] -> H8)
    :return: algebraic notation
    """
    if (0 <= coord[0] <= 7) and (0 <= coord[1] <= 7):
        row = str(coord[0] + 1)
        col = chr(coord[1] + 65)
        return col + row
    else:
        return None


def coordListToAlgebra(coordList: list[npt.NDArray[int]] | list[tuple]) -> list[str] | None:
    """
    converts a list of sets of coordinates into algebraic notation
    :param coordList: set of coordinates to be converted into algebraic notation (e.g. [0,0] -> A1, [7,7] -> H8)
    :return: algebraic notation
    """
    retList = []
    for coord in coordList:
        row = str(coord[0] + 1)
        col = chr(coord[1] + 65)
        retList.append(col + row)
    if len(retList) != 0:
        return retList
    else:
        return None


def vector(coord0: npt.NDArray[int], coord1: npt.NDArray[int]) -> tuple[npt.NDArray[int], int] | None:
    """
    converts the direction between a piece at a given set of coordinates and that at another given set of coordinates into a direction vector
    :param coord0: set of coordinates of the first piece
    :param coord1: set of coordinates of the second piece
    :return: direction vector
    """
    if (0 <= coord0[0] <= 7) and (0 <= coord0[1] <= 7) and (0 <= coord1[0] <= 7) and (0 <= coord1[1] <= 7):
        diffVector = coord1 - coord0
        absTotal = abs(diffVector[0]) + abs(diffVector[1])
        if absTotal == 3 and diffVector[0] != 0 and diffVector[1] != 0:
            return diffVector, 1
        elif abs(diffVector[0]) == abs(diffVector[1]):
            return (diffVector / (absTotal / 2)).astype(int), int(absTotal / 2)
        elif absTotal == abs(diffVector[0]) or absTotal == abs(diffVector[1]):
            return (diffVector / absTotal).astype(int), absTotal
        else:
            return None
    else:
        return None


def arrayInList(arr: npt.NDArray[Any], lst: list[npt.NDArray[Any]]) -> bool:
    """
    checks if an array is in a list of arrays and returns a bool
    :param arr: array to check for
    :param lst: list of arrays to check
    :return:
    """
    if lst is None:
        return False
    else:
        return any(np.array_equal(arr, elem) for elem in lst)


def removeArray(arr: npt.NDArray[Any], lst: list[npt.NDArray[Any]]) -> None:
    """
    removes an array from a list of arrays
    :param arr: array to remove
    :param lst: list of arrays to remove from
    :return:
    """
    ind = 0
    size = len(lst)
    while ind != size and not np.array_equal(lst[ind], arr):
        ind += 1
    if ind != size:
        lst.pop(ind)
