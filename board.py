from typing import Any, Callable, Optional

from piece import Piece
from piece import King
import errors
import numpy as np
import numpy.typing as npt
from collections import Counter

"""             
    chess variants to add (use inheritance):
        giveaway https://www.chess.com/terms/giveaway-chess (no castle, no check, king is not royal, promotionOptions = ['r', 'b', 'q', 'n', 'k'], custom win condition)
        atomic? https://www.chess.com/terms/atomic-chess
        960 https://www.chess.com/terms/chess960 (see https://en.wikipedia.org/wiki/Fischer_random_chess#Creating_starting_positions for generation algorithm)
        3-check? (new UI elements) https://www.chess.com/terms/3-check-chess
        crazyhouse? (new UI elements) https://www.chess.com/terms/crazyhouse-chess
        duck (new piece, new interface prompts) https://www.chess.com/terms/duck-chess (no check, stalemateWinnerMult=1) 
        gothic (new piece, 10x8 board) https://www.chess.com/terms/gothic-chess
        horde? https://www.chess.com/terms/horde-chess
        no castling https://www.chess.com/terms/no-castling-chess (no castling)
        4-player? https://www.chess.com/terms/4-player-chess
        torpedo https://www.chess.com/terms/torpedo-chess (different pawn movement)
        xxl (new piece, bigger board) https://www.chess.com/terms/xxl-chess (no ep)
    chess variant (normal, ?giveaway, ?atomic, !960, ?3-check, ?crazyhouse, ?duck, ?gothic, ?horde, ?no castling, ?xxl) REMOVE QUESTION MARK FOR A VARIANT WHEN IT IS FULLY IMPLEMENTED
"""


# TODO: big things: rewrite without numpy

class Board:
    @staticmethod
    def defaultStart() -> list[str]:
        """
        starting board layout
        :return:
        """
        return ["rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", 'w', "KQkq", '-', '0', '1']

    @property
    def xSize(self) -> int:
        """
        x-axis size of the board (number of columns/files)
        :return:
        """
        return 8

    @property
    def ySize(self) -> int:
        """
        y-axis size of the board (number of rows/ranks)
        :return:
        """
        return 8

    def nthRowForColor(self, n: int, color: int) -> int:
        """
        finds the nth row for a given color (0-indexed)
        :param n: row number
        :param color: color to start from the side of
        :return:
        """
        return int((self.ySize - 1) / 2 - color * (self.ySize - 1 - 2 * n) / 2)

    @property
    def singleSquareVectorDict(self) -> dict[str, list[npt.NDArray[int]] | None]:
        """
        dictionary of single square moves for each piece
        :return:
        """
        return self._singleSquareVectorDict

    @singleSquareVectorDict.setter
    def singleSquareVectorDict(self, none) -> None:
        self._singleSquareVectorDict = {
            'k': [np.array([1, 0]), np.array([1, 1]), np.array([0, 1]), np.array([-1, 1]), np.array([-1, 0]),
                  np.array([-1, -1]), np.array([0, -1]), np.array([1, -1])],
            'n': [np.array([2, 1]), np.array([1, 2]), np.array([-1, 2]), np.array([-2, 1]), np.array([-2, -1]),
                  np.array([-1, -2]), np.array([1, -2]), np.array([2, -1])], 'q': None, 'b': None, 'r': None, 'p': None}

    @property
    def multiSquareVectorDict(self) -> dict[str, list[npt.NDArray[int]] | None]:
        """
        dictionary of multiple square move directions for each piece
        :return:
        """
        return self._multiSquareVectorDict

    @multiSquareVectorDict.setter
    def multiSquareVectorDict(self, none) -> None:
        self._multiSquareVectorDict = {'k': None, 'n': None,
                                       'q': [np.array([1, 0]), np.array([1, 1]), np.array([0, 1]), np.array([-1, 1]),
                                             np.array([-1, 0]), np.array([-1, -1]), np.array([0, -1]),
                                             np.array([1, -1])],
                                       'b': [np.array([1, 1]), np.array([-1, 1]), np.array([-1, -1]),
                                             np.array([1, -1])],
                                       'r': [np.array([1, 0]), np.array([0, 1]), np.array([-1, 0]), np.array([0, -1])],
                                       'p': None}

    @property
    def startCastlingLocationDict(self) -> dict[int, npt.NDArray | None]:
        """
        dictionary for rook and king initial locations (order is queen side rook, king, king side rook)
        :return:
        """
        return self._startCastlingLocationDict

    @startCastlingLocationDict.setter
    def startCastlingLocationDict(self, none) -> None:
        self._startCastlingLocationDict = {-1: [np.array([7, 0]), np.array([7, 4]), np.array([7, 7])],
                                           1: [np.array([0, 0]), np.array([0, 4]), np.array([0, 7])]}

    @property
    def promotionRow(self) -> int:
        """
        int specifying the row number that promotions happen at (from white's perspective)
        :return:
        """
        return 7

    @property
    def promotionTypes(self) -> list[str]:
        """
        types of pieces that can be promoted to
        :return:
        """
        return ['r', 'b', 'q', 'n']

    @property
    def promotionNames(self) -> list[str]:
        """
        full names of types of pieces that can be promoted to
        :return:
        """
        return ['rook', 'bishop', 'queen', 'knight']

    @staticmethod
    def promotionNameToType(name: str) -> str | None:
        """
        converts the full name of a piece that can be promoted to to its type
        :param name: full name of the piece
        :return:
        """
        promotionType = name[0]
        if promotionType == 'k':
            promotionType = 'n'
        return promotionType

    @property
    def usesCheck(self) -> bool:
        """
        bool specifying whether check is used
        :return:
        """
        return True

    @property
    def usesCastling(self) -> bool:
        """
        bool specifying whether castling is used
        :return:
        """
        return True

    @property
    def usesEPAtAll(self) -> bool:
        """
        bool specifying whether en passant is used
        :return:
        """
        return True

    @property
    def kingIsRoyal(self) -> bool:
        """
        bool specifying whether the king's capture ends the game
        :return:
        """
        return True

    @property
    def stalemateWinnerMult(self) -> int:
        """
        int specifying who wins in case of a stalemate (0 for draw, 1 for player who is about to move, -1 for player who just moved)
        :return:
        """
        return 0

    def variantGameWinCondition(self) -> int | None:
        pass

    def __init__(self, customBoard: list[str] = None, customStart: list[str] = None):
        """
        initializes the board
        :param customBoard: custom board in FEN format (list of strings)
        :param customStart: list of starting moves; will default to none
        """
        self.turnColor, self.castleChecks, self.kingDict, self.checkMoveDict, self.epList, self.halfMoveNum, self.fullMoveNum, self.fenLog, self.algList = 1, {}, {}, {}, [], 0, 1, [], []
        self.board: npt.NDArray[[Piece]] | None = None
        self.epCoord: npt.NDArray[int] | None = None
        self.singleSquareVectorDict, self.multiSquareVectorDict, self.startCastlingLocationDict = None, None, None
        startFen = customBoard if customBoard is not None else self.defaultStart()
        self.pList = [np.array((0, -1)), np.array((0, 1))]
        self.setFromFEN(startFen)
        if customStart is not None:
            for move in customStart:
                endStrPos = 1
                while move[endStrPos].isdigit():
                    endStrPos += 1
                startAlg = move[0:endStrPos]
                promo = move[-1] if move[-1].isalpha() else None
                endAlg = move[endStrPos:] if promo is None else move[endStrPos:-1]
                startCoord = self.algebraToCoordinates(startAlg)
                endCoord = self.algebraToCoordinates(endAlg)
                if self.moveIsValid(startCoord, endCoord):
                    self.updateMoves(startCoord, endCoord, promotionType=promo)

    def __str__(self) -> str:
        """
        converts to string
        :return:
        """

        retStr = "\033[0m  "
        for col in range(self.xSize):
            retStr += "   " + chr(col + 97)
        retStr += "\n\033[0m   ┌"
        for col in range(self.xSize - 1):
            retStr += "───┬"
        retStr += "───┐"
        for row in range(self.ySize * 2 - 1, 0, -1):
            match row % 2:
                case 1:
                    retStr += "\n " + str(int((row + 1) / 2)) + " "
                    for col in range(self.xSize):
                        retStr += "\033[0m│\033[0m " + self.charAt((int((row - 1) / 2), col)) + " "
                    retStr += "\033[0m│ " + str(int((row + 1) / 2)) + " "
                case 0:
                    retStr += "\n\033[0m   ├"
                    for col in range(self.xSize - 1):
                        retStr += "───┼"
                    retStr += "───┤"
        retStr += "\n\033[0m   └"
        for col in range(self.xSize - 1):
            retStr += "───┴"
        retStr += "───┘"
        retStr += "\n\033[0m  "
        for col in range(self.xSize):
            retStr += "   " + chr(col + 97)
        return retStr

    def toFEN(self) -> list[str]:
        fenList = []
        boardString = ""
        for y in range(self.ySize - 1, -1, -1):
            blankLen = 0
            for x in range(self.xSize):
                if self.colorAt((y, x)):
                    if blankLen != 0:
                        boardString += str(blankLen)
                        blankLen = 0
                    boardString += self.typeAt((y, x)).upper() if self.colorAt((y, x)) == 1 else self.typeAt((y, x))
                else:
                    blankLen += 1
            if blankLen != 0:
                boardString += str(blankLen)
            boardString += "/"
        boardString.removesuffix("/")
        fenList.append(boardString)
        fenList.append('w') if self.turnColor == 1 else fenList.append('b')
        castleString = ""
        if self.castleChecks[1][2] and self.castleChecks[1][1]:
            castleString += 'K'
        if self.castleChecks[1][0] and self.castleChecks[1][1]:
            castleString += 'Q'
        if self.castleChecks[-1][2] and self.castleChecks[-1][1]:
            castleString += 'k'
        if self.castleChecks[-1][0] and self.castleChecks[-1][1]:
            castleString += 'q'
        fenList.append("-") if len(castleString) == 0 else fenList.append(castleString)
        fenList.append(self.coordToAlgebra(self.epCoord)) if self.epCoord is not None else fenList.append("-")
        fenList.append(str(self.halfMoveNum))
        fenList.append(str(self.fullMoveNum))
        return fenList

    def setFromFEN(self, fen: list[str]) -> None:
        self.board = np.array(
            [np.fromiter((Piece(None, 0) for j in range(self.xSize)), dtype=Piece) for i in range(self.ySize)])
        boardList = fen[0].split("/")
        for y in range(self.ySize - 1, -1, -1):
            x = 0
            curBlankStr = ""
            for c in boardList[self.ySize - y - 1]:
                if c.isdigit():
                    curBlankStr += c
                else:
                    if len(curBlankStr) != 0:
                        x += int(curBlankStr)
                        curBlankStr = ""
                    curColor = 1 if c.isupper() else -1
                    self.board[(y, x)] = Piece(c.lower(), curColor)
                    x += 1
        self.turnColor = 1 if fen[1] == 'w' else -1
        self.castleChecks = {-1: [False for _ in range(3)], 1: [False for _ in range(3)]}
        if 'K' in fen[2]:
            self.castleChecks[1][2] = True
            self.castleChecks[1][1] = True
        if 'Q' in fen[2]:
            self.castleChecks[1][0] = True
            self.castleChecks[1][1] = True
        if 'k' in fen[2]:
            self.castleChecks[-1][2] = True
            self.castleChecks[-1][1] = True
        if 'q' in fen[2]:
            self.castleChecks[-1][0] = True
            self.castleChecks[-1][1] = True
        self.kingDict = {}
        self.checkMoveDict = {}
        self.epList = []
        self.epCoord = self.algebraToCoordinates(fen[3]) if fen[3] != '-' else None
        self.halfMoveNum = int(fen[4])
        self.fullMoveNum = int(fen[5])
        self.fenLog = []
        self.initMoves()
        if self.usesCheck and self.inCheck(self.kingDict[self.turnColor].position, self.turnColor):
            self.kingDict[self.turnColor].inCheck = True
            self.enterCheckMode(self.turnColor)
        self.algList = []

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
        return True if arrayInList(move, self.board[tuple(coord)].moveList) else False

    def canMoveToBools(self, coord: npt.NDArray[int] | tuple, moves: list[npt.NDArray[int]]) -> list[bool]:
        """
        checks if a piece at a given set of coordinates can move to a given list of sets of coordinates and returns a list of bools
        :param coord: coordinates of the initial set of coordinates of the piece
        :param moves: list of sets of coordinates to check if the piece can move to
        :return: bool
        """
        retList = []
        for move in moves:
            retList.append(True) if arrayInList(move, self.board[tuple(coord)].moveList) else retList.append(False)
        return retList

    def canMoveList(self, coord: npt.NDArray[int] | tuple) -> list[npt.NDArray[int]]:
        """
        returns a list of the sets of coordinates of all pieces that can move to a given set of coordinates
        :param coord: coordinates to check if pieces can move to
        :return: list of the sets of coordinates of all pieces that can move to the given set of coordinates
        """
        squareList = []
        for i in range(self.xSize):
            for j in range(self.ySize):
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
        return True if arrayInList(block, self.board[tuple(coord)].blockList) else False

    def blockedAtBools(self, coord: npt.NDArray[int] | tuple, blocks: list[npt.NDArray[int]]) -> list[bool]:
        """
        checks if a piece at a given set of coordinates is blocked at a given list of sets of coordinates and returns a list of bools
        :param coord: coordinates of the initial set of coordinates of the piece
        :param blocks: list of sets of coordinates to check if the piece is blocked at
        :return: bool
        """
        retList = []
        for block in blocks:
            retList.append(True) if arrayInList(block, self.board[tuple(coord)].blockList) else retList.append(False)
        return retList

    def blockedAtList(self, coord: npt.NDArray[int] | tuple) -> list[npt.NDArray[int]]:
        """
        returns a list of the sets of coordinates of all pieces that are blocked at a given set of coordinates
        :param coord: coordinates to check if pieces are blocked at
        :return: list of the sets of coordinates of all pieces that are blocked at the given set of coordinates
        """
        squareList = []
        for i in range(self.xSize):
            for j in range(self.ySize):
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
        return True if arrayInList(capture, self.board[tuple(coord)].captureList) else False

    def capturedAtBools(self, coord: npt.NDArray[int] | tuple, captures: list[npt.NDArray[int]]) -> list[bool]:
        """
        checks if a piece at a given set of coordinates has a capture at a given list of sets of coordinates and returns a list of bools
        :param coord: coordinates of the initial set of coordinates of the piece
        :param captures: list of sets of coordinates to check if the piece has a capture
        :return: bool
        """
        retList = []
        for capture in captures:
            retList.append(True) if arrayInList(capture, self.board[tuple(coord)].captureList) else retList.append(
                False)
        return retList

    def capturedList(self, coord: npt.NDArray[int] | tuple) -> list[npt.NDArray[int]]:
        """
        returns a list of the sets of coordinates of all pieces that have a capture at a given set of coordinates
        :param coord: coordinates to check if pieces can capture
        :return: list of the sets of coordinates of all pieces that have a capture at the given set of coordinates
        """
        squareList = []
        for i in range(self.xSize):
            for j in range(self.ySize):
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
            if self.xSize > ep[1] + v[1] >= 0 and self.typeAt((ep[0] + color, ep[1] + v[1])) == 'p' and self.colorAt(
                    (ep[0] + color, ep[1] + v[1])) * color == -1 and self.colorAt(ep) == 0:
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
        return True if self.usesEPAtAll and self.epCoord is not None and arrayInList(startCoord,
                                                                                     self.epList) and np.array_equal(
            self.epCoord, endCoord) else False

    def iterateUntilNextOccupiedSquare(self, startCoord: npt.NDArray[int], dirVector: npt.NDArray[int],
                                       squareFunc: Optional[Callable], *args, skipCoord: npt.NDArray[int] = None,
                                       stopCoord: npt.NDArray[int] = None, stopForCheckColor: int = 0, **kwargs) -> \
            npt.NDArray[int] | None:
        """
        iterates over the board from a starting square in a direction until it hits an occupied square, calling a function on all squares in the middle, and returns the occupied square
        :param startCoord: square to start from (exclusive)
        :param dirVector: vector to iterate with
        :param squareFunc: function to call on squares in the middle
        :param skipCoord: optional coordinate to ignore color at
        :param stopCoord: optional coordinate to stop at if reached
        :param stopForCheckColor: int for whether to stop if square is in check and color to use
        :return:
        """
        curPos = startCoord + dirVector
        while 0 <= curPos[0] < self.ySize and 0 <= curPos[1] < self.xSize and (
                not self.colorAt(curPos) or (skipCoord is not None and np.array_equal(curPos, skipCoord))) and (
                stopCoord is None or not np.array_equal(curPos, stopCoord)) and not (
                stopForCheckColor and self.inCheck(curPos, stopForCheckColor)):
            if squareFunc is not None:
                squareFunc(*args, curPos.copy(), **kwargs)
            curPos += dirVector
        else:
            return curPos if 0 <= curPos[0] < self.ySize and 0 <= curPos[1] < self.xSize else None

    def pawnCanDoubleMove(self, coord: npt.NDArray[int] | tuple) -> bool:
        """
        checks if a pawn at a given set of coordinates can make a double move
        :param coord: coordinates of the pawn to check if it can double move
        :return:
        """
        return True if coord[0] == self.nthRowForColor(1, self.colorAt(coord)) else False

    def generatePawnListAt(self, coord: npt.NDArray[int] | tuple) -> None:
        """
        generates the moveList, blockList, and captureList at a given set of coordinates of a pawn
        :param coord: coordinates of the pawn whose lists will be generated
        :return:
        """
        moveList = []
        blockList = []
        captureList = []
        color = self.colorAt(coord)
        y: int = coord[0]
        x: int = coord[1]
        if not self.colorAt((y + color, x)):
            moveList.append(np.array([y + color, x]))
            if self.pawnCanDoubleMove(coord):
                blockList.append(np.array([y + 2 * color, x])) if self.colorAt((y + 2 * color, x)) else moveList.append(
                    np.array([y + 2 * color, x]))
        else:
            blockList.append(np.array([y + color, x]))
        for i in [-1, 1]:
            if 0 <= x + i < self.xSize and self.colorAt((y + color, x + i)) * color == -1:
                captureList.append(np.array([y + color, x + i]))
        self.addMovesAt(coord, moveList)
        self.addBlocksAt(coord, blockList)
        self.addCapturesAt(coord, captureList)

    def generateListsAt(self, coord: npt.NDArray[int] | tuple) -> None:
        """
        generates the moveList, blockList, and captureList at a given set of coordinates
        :param coord: coordinates of the piece whose lists will be generated
        :return:
        """
        moveList = []
        blockList = []
        captureList = []
        curType = self.typeAt(coord)
        color = self.colorAt(coord)
        arrayCoord = np.array(coord) if type(coord) == tuple else coord
        if curType == 'p':
            self.generatePawnListAt(coord)
        elif curType is not None:
            if curType == 'k' and self.usesCheck:
                inCheck = self.inCheck(coord, color)
                self.kingDict[self.colorAt(coord)] = King(inCheck, arrayCoord)
            if self.singleSquareVectorDict[curType] is not None:
                for v in self.singleSquareVectorDict[curType]:
                    curPos = arrayCoord + v
                    if 0 <= curPos[0] < self.ySize and 0 <= curPos[1] < self.xSize:
                        blockList.append(curPos) if color * self.colorAt(curPos) == 1 else captureList.append(
                            curPos) if color * self.colorAt(curPos) == -1 else moveList.append(curPos)
            if self.multiSquareVectorDict[curType] is not None:
                for v in self.multiSquareVectorDict[curType]:
                    endPos = self.iterateUntilNextOccupiedSquare(arrayCoord, v, moveList.append)
                    if endPos is not None:
                        blockList.append(endPos) if self.colorAt(endPos) * color == 1 else captureList.append(endPos)
        self.addMovesAt(coord, moveList)
        self.addBlocksAt(coord, blockList)
        self.addCapturesAt(coord, captureList)

    def initMoves(self) -> None:
        """
        initializes the moveLists, blockLists, and captureLists
        :return:
        """
        for y in range(self.ySize):
            for x in range(self.xSize):
                self.generateListsAt((y, x))
        if self.epCoord is not None:
            self.setEP(self.epCoord, self.turnColor * -1)
        if self.usesCastling:
            for color in [-1, 1]:
                self.addMovesAt(self.startCastlingLocationDict[color][1],
                                self.validCastleOptions(color, useCheck=False))

    def addPieceAt(self, coord: npt.NDArray[int], pieceType: str, color: int) -> None:
        """
        adds a piece to a given set of coordinates and updates moveLists, blockLists, and captureLists
        :param coord: coordinates to add the piece
        :param pieceType: type of the piece to add
        :param color: color of the piece to add
        :return:
        """
        oldColor = self.colorAt(coord)
        if self.usesCastling and (coord[0] == 0 or coord[0] == self.ySize - 1) and oldColor == 0:
            castleColor = 1 if coord[0] == 0 else -1
            if self.castleChecks[castleColor][1]:
                self.removeMovesAt(self.startCastlingLocationDict[color][1],
                                   self.validCastleOptions(color, useCheck=False))
        self.board[tuple(coord)] = Piece(pieceType, color)
        match oldColor:
            case 0:
                updateList = self.canMoveList(coord)
                for square in updateList:
                    curType = self.typeAt(square)
                    curColor = self.colorAt(square)
                    dirVec = self.vector(square, coord)
                    if curType == 'p':
                        self.removeMoveAt(square, coord)
                        self.addBlockAt(square, coord)
                        curPos = dirVec[0] + coord
                        if self.canMoveTo(square, curPos):
                            self.removeMoveAt(square, curPos)
                    elif curType is not None:
                        self.removeMoveAt(square, coord)
                        self.addBlockAt(square, coord) if curColor * color == 1 else self.addCaptureAt(square, coord)
                        if self.multiSquareVectorDict[curType] is not None:
                            endPos = self.iterateUntilNextOccupiedSquare(coord, dirVec[0], self.removeMoveAt, square)
                            if endPos is not None:
                                self.removeBlockAt(square, endPos) if self.colorAt(
                                    endPos) * color == 1 else self.removeCaptureAt(square, endPos)
                if self.usesCastling and (coord[0] == 0 or coord[0] == self.ySize - 1):
                    castleColor = 1 if coord[0] == 0 else -1
                    if self.castleChecks[castleColor][1]:
                        self.addMovesAt(self.startCastlingLocationDict[color][1],
                                        self.validCastleOptions(color, useCheck=False))
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
            if 0 <= pawnPos[0] < self.ySize and 0 <= pawnPos[1] + i < self.xSize and self.colorAt(
                    pawnPos) * color == -1 and self.typeAt(pawnPos) == 'p':
                self.addCaptureAt(pawnPos, coord)
        self.generateListsAt(coord)
        if pieceType == 'k' and self.usesCheck:
            self.kingDict[color].position = coord

    def removePieceAt(self, coord: npt.NDArray[int]) -> None:
        """
        removes a piece from a given set of coordinates and updates moveLists, blockLists, and captureLists (technically replaces it with an empty piece)
        :param coord: coordinates to remove the piece from
        :return:
        """
        color = self.colorAt(coord)
        updateList = self.blockedAtList(coord) + self.capturedList(coord)
        if self.usesCastling and indexOfArrayInList(coord, self.startCastlingLocationDict[color]) is not None and (
                self.typeAt(coord) == 'r' or self.typeAt(coord) == 'k'):
            self.castleChecks[color][indexOfArrayInList(coord, self.startCastlingLocationDict[color])] = False
        if self.typeAt(coord) == 'k' and self.kingIsRoyal:
            errors.GameOver(color * -1)
        if self.usesCastling and (coord[0] == 0 or coord[0] == self.ySize - 1):
            castleColor = 1 if coord[0] == 0 else -1
            if self.castleChecks[castleColor][1]:
                self.removeMovesAt(self.startCastlingLocationDict[color][1],
                                   self.validCastleOptions(color, useCheck=False))
        self.board[tuple(coord)] = Piece(None, 0)
        if self.usesCastling and (coord[0] == 0 or coord[0] == self.ySize - 1):
            castleColor = 1 if coord[0] == 0 else -1
            if self.castleChecks[castleColor][1]:
                self.addMovesAt(self.startCastlingLocationDict[color][1],
                                self.validCastleOptions(color, useCheck=False))
        for square in updateList:
            curType = self.typeAt(square)
            curColor = self.colorAt(square)
            dirVec = self.vector(square, coord)
            if curType == 'p':
                if square[0] != coord[0]:
                    match square[1] - coord[1]:
                        case 0:
                            self.removeBlockAt(square, coord)
                            self.addMoveAt(square, coord)
                            if self.pawnCanDoubleMove(square) and coord[0] == square[0] + color:
                                curPos = dirVec[0] + coord
                                self.addMoveAt(square, curPos) if color * self.colorAt(
                                    curPos) == 0 else self.addBlockAt(square, curPos)
                        case 1 | -1:
                            self.removeCaptureAt(square, coord)
            elif curType is not None:
                self.addMoveAt(square, coord)
                self.removeBlockAt(square, coord) if curColor * color == 1 else self.removeCaptureAt(square, coord)
                if self.multiSquareVectorDict[curType] is not None:
                    endPos = self.iterateUntilNextOccupiedSquare(coord, dirVec[0], self.addMoveAt, square)
                    if endPos is not None:
                        self.addBlockAt(square, endPos) if self.colorAt(endPos) * color == 1 else self.addCaptureAt(
                            square, endPos)

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
                                    square[0] == startCoord[0] and arrayInList(self.pList[0],
                                                                               self.multiSquareVectorDict[
                                                                                   self.typeAt(square)])]
            for square in epDoubleExposureList:
                dirVec = self.vector(square, startCoord)
                startPos = np.array((startCoord[0], endCoord[1] + (
                        np.sign(dirVec[0][1]) * (endCoord[1] - startCoord[1]) * 0.5 - 0.5) * np.sign(dirVec[0][1])))
                endPos = self.iterateUntilNextOccupiedSquare(startPos, dirVec[0], None)
                if np.array_equal(endPos, kingCoord):
                    return True
            epExposureList = [square for square in epExposureList if not arrayInList(square, epDoubleExposureList)]
            for square in epExposureList:
                curType = self.typeAt(square)
                if self.multiSquareVectorDict[curType] is not None:
                    dirVec = self.vector(square, epCapCoord)
                    endPos = self.iterateUntilNextOccupiedSquare(square, dirVec[0], None, skipCoord=epCapCoord,
                                                                 stopCoord=endCoord)
                    if np.array_equal(endPos, kingCoord):
                        return True
            exposureList = [square for square in exposureList if not arrayInList(square, epDoubleExposureList)]
        for square in exposureList:
            curType = self.typeAt(square)
            if self.multiSquareVectorDict[curType] is not None:
                dirVec = self.vector(square, startCoord)
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
                if self.multiSquareVectorDict[curType] is not None:
                    dirVec = self.vector(square, kingCoord)
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
        for y in range(self.ySize):
            for x in range(self.xSize):
                if self.colorAt((y, x)) == color:
                    if self.typeAt((y, x)) == 'k':
                        optionList = []
                        blockList = self.blocksAt(kingCoord)
                        for v in self.singleSquareVectorDict['k']:
                            curPos = kingCoord + v
                            if 0 <= curPos[0] < self.ySize and 0 <= curPos[1] < self.xSize and not self.inCheck(curPos,
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
        elif not 0 <= coord[0] < self.ySize or not 0 <= coord[1] < self.xSize:
            raise errors.InvalidMoveOffBoard
        elif self.usesCheck and self.kingDict[color].inCheck:
            if tuple(coord) in self.checkMoveDict.keys():
                return True
            else:
                raise errors.InvalidMoveCheck
        optionList = self.validMoveOptions(coord)
        if optionList:
            return True
        else:
            raise errors.PieceCantMove

    def validCastleOptions(self, color: int, useCheck: bool = None) -> list[npt.NDArray[int]]:
        """
        returns a list of moves that are valid and perform a castle
        :param color: color of the pieces to check
        :param useCheck: bool for if to care about check (defaults to self.usesCheck)
        :return:
        """
        if useCheck is None:
            useCheck = self.usesCheck
        kingStartCoord = self.startCastlingLocationDict[color][1]
        retList = []
        if useCheck and self.inCheck(kingStartCoord, color):
            return retList
        for i in [0, 2]:
            if self.castleChecks[color][1] and self.castleChecks[color][i]:
                kingEndCoord = np.array([self.nthRowForColor(0, color), 2 if i == 0 else self.xSize - 2])
                kv = self.vector(kingStartCoord, kingEndCoord)[0]
                rookStartCoord = self.startCastlingLocationDict[color][i]
                curCoord = self.iterateUntilNextOccupiedSquare(kingStartCoord, kv, None, skipCoord=rookStartCoord,
                                                               stopCoord=kingEndCoord,
                                                               stopForCheckColor=color if useCheck else 0)
                if np.array_equal(curCoord, kingEndCoord) and not (useCheck and self.inCheck(curCoord, color)):
                    rookEndCoord = np.array([self.nthRowForColor(0, color), 3 if i == 0 else self.xSize - 3])
                    rv = self.vector(rookStartCoord, rookEndCoord)[0]
                    curCoord = self.iterateUntilNextOccupiedSquare(rookStartCoord, rv, None, skipCoord=kingStartCoord,
                                                                   stopCoord=rookEndCoord)
                    if np.array_equal(curCoord, rookEndCoord):
                        retList.append(kingEndCoord)
        return retList

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
        elif not 0 <= startCoord[0] < self.ySize or not 0 <= startCoord[1] < self.xSize or not 0 <= endCoord[
            0] < self.ySize or not 0 <= endCoord[1] < self.xSize:
            raise errors.InvalidMoveOffBoard
        elif pieceType == 'k' and self.usesCastling and arrayInList(endCoord, self.validCastleOptions(color)):
            return True
        elif self.colorAt(endCoord) * color == 1:
            raise errors.InvalidMoveBlocked
        elif self.usesCheck and self.kingDict[color].inCheck:
            if tuple(startCoord) in self.checkMoveDict.keys():
                if arrayInList(endCoord, self.checkMoveDict[tuple(startCoord)]):
                    return True
                else:
                    raise errors.InvalidMoveCheck
            else:
                raise errors.InvalidMoveCheck
        elif self.usesCheck and self.exposesKing(startCoord, endCoord, self.kingDict[color].position, color):
            raise errors.InvalidMoveIntoCheck
        elif pieceType == 'k':
            if not (self.usesCheck and self.inCheck(endCoord, color)) and (
                    self.canMoveTo(startCoord, endCoord) or self.capturedAt(startCoord, endCoord)):
                return True
            else:
                raise errors.InvalidMoveGeneric
        elif pieceType == 'p' and self.usesEPAtAll and self.usesEP(startCoord, endCoord):
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
            if self.usesCheck and self.kingDict[color].inCheck and tuple(
                    coord) in self.checkMoveDict.keys() and arrayInList(square, self.checkMoveDict[tuple(coord)]):
                retList.append(square)
            elif self.usesCheck and self.exposesKing(coord, square, self.kingDict[color].position, color):
                pass
            elif pieceType == 'k':
                if self.usesCastling and arrayInList(square, self.validCastleOptions(color)):
                    retList.append(square)
                elif not (self.usesCheck and self.inCheck(square, color)) and (
                        self.canMoveTo(coord, square) or self.capturedAt(coord, square)):
                    retList.append(square)
            elif pieceType == 'p' and self.usesEPAtAll and self.usesEP(coord, square):
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
        if self.usesCheck and self.kingDict[self.turnColor].inCheck:
            return [np.array(coord) for coord in list(self.checkMoveDict.keys())]
        for y in range(self.ySize):
            for x in range(self.xSize):
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
        for y in range(self.ySize):
            for x in range(self.xSize):
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

    def nRepetitions(self, n: int) -> bool:
        """
        checks if any board state has repeated at least n times
        :return:
        """
        if len(self.fenLog) == 0:
            return False
        else:
            fenLogShort = tuple(tuple(fen[0:4]) for fen in self.fenLog)
            fenCounter = Counter(fenLogShort)
            return True if fenCounter.most_common(1)[0][1] >= n else False

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
            self.halfMoveNum = 0
        else:
            self.halfMoveNum += 1
        if pieceType == 'k' and arrayInList(endCoord, self.validCastleOptions(color)):
            self.castleChecks[color][1] = False
            self.castleChecks[color][0 if endCoord[1] == 2 else 2] = False
            rookStartCoord = self.startCastlingLocationDict[0 if endCoord[1] == 2 else 2]
            rookEndCoord = np.array([startCoord[0], 3]) if endCoord[1] == 2 else np.array(
                [startCoord[0], self.xSize - 3])
            self.removePieceAt(rookStartCoord)
            self.addPieceAt(rookEndCoord, 'r', color)
        elif pieceType == 'p' and self.usesEPAtAll and self.usesEP(startCoord, endCoord):
            self.removePieceAt(np.array((self.epCoord[0] - color, self.epCoord[1])))
        elif (pieceType == 'k' or pieceType == 'r') and self.nthRowForColor(0, color):
            posList = [square[1] for square in self.startCastlingLocationDict[color]]
            if startCoord[1] in posList:
                self.castleChecks[color][posList.index(startCoord[1])] = False
        self.removePieceAt(startCoord)
        if pieceType == 'p' and endCoord[0] == self.nthRowForColor(self.promotionRow, color):
            self.addPieceAt(endCoord, promotionType, color) if promotionType else self.addPieceAt(endCoord, 'q', color)
        else:
            self.addPieceAt(endCoord, pieceType, color)
        self.setEP((endCoord[0] - color, endCoord[1]), color) if pieceType == 'p' and self.usesEPAtAll and (
                endCoord[0] - startCoord[0]) * color == 2 else self.clearEP()
        if self.usesCheck:
            self.checkMoveDict.clear()
            for i in [-1, 1]:
                self.kingDict[i].inCheck = self.inCheck(self.kingDict[i].position, i)
                if self.kingDict[i].inCheck:
                    self.enterCheckMode(i)
            if self.turnColor == -1:
                self.fullMoveNum += 1
        self.turnColor *= -1
        self.algList.append(self.coordToAlgebra(startCoord) + self.coordToAlgebra(endCoord) + str(promotionType or ""))
        self.fenLog.append(self.toFEN())

    def printStatus(self, printMoves: bool = True, printBlocks: bool = True, printCaptures: bool = True):
        for y in range(self.ySize):
            for x in range(self.xSize):
                print(str(self.coordToAlgebra((y, x))) + ": " + str(self.typeAt((y, x))) + " " + str(
                    self.colorAt((y, x))))
                if printMoves:
                    print("Moves: " + str(self.movesAt((y, x))))
                if printBlocks:
                    print("Blocks: " + str(self.blocksAt((y, x))))
                if printCaptures:
                    print("Captures: " + str(self.capturesAt((y, x))))

    def algebraToCoordinates(self, algebra: str) -> npt.NDArray[int] | None:
        """
        converts algebraic notation into a set of coordinates
        :param algebra: algebraic notation to be converted into a set of coordinates (e.g. A1 -> [0,0], A8 -> [0,7], H8 -> [7,7])
        :return: set of coordinates
        """
        if len(algebra) < 2:
            return None
        col = ord(algebra[0].lower()) - 97
        rowStr = algebra[1:]
        if col < 0 or col > 25 or not rowStr.isdecimal():
            raise errors.InvalidSyntax
        row = int(rowStr) - 1
        if 0 <= row < self.ySize and 0 <= col < self.xSize:
            retNP = np.array((row, col))
            return retNP
        raise errors.InvalidSyntax

    def coordToAlgebra(self, coord: npt.NDArray[int] | tuple) -> str | None:
        """
        converts a set of coordinates into algebraic notation
        :param coord: set of coordinates to be converted into algebraic notation (e.g. [0,0] -> A1, [7,7] -> H8)
        :return: algebraic notation
        """
        if 0 <= coord[0] < self.ySize and 0 <= coord[1] < self.xSize:
            row = str(coord[0] + 1)
            col = chr(coord[1] + 97)
            return col + row
        return None

    def coordListToAlgebra(self, coordList: list[npt.NDArray[int]] | list[tuple]) -> list[str] | None:
        """
        converts a list of sets of coordinates into algebraic notation
        :param coordList: set of coordinates to be converted into algebraic notation (e.g. [0,0] -> A1, [7,7] -> H8)
        :return: algebraic notation
        """
        retList = []
        for coord in coordList:
            if 0 <= coord[0] < self.ySize and 0 <= coord[1] < self.xSize:
                row = str(coord[0] + 1)
                col = chr(coord[1] + 97)
                retList.append(col + row)
            else:
                return None
        return retList if len(retList) != 0 else None

    def vector(self, coord0: npt.NDArray[int], coord1: npt.NDArray[int]) -> tuple[npt.NDArray[int], int] | None:
        """
        converts the direction between a piece at a given set of coordinates and that at another given set of coordinates into a direction vector
        :param coord0: set of coordinates of the first piece
        :param coord1: set of coordinates of the second piece
        :return: direction vector
        """
        if 0 <= coord0[0] < self.ySize and 0 <= coord0[1] < self.xSize and 0 <= coord1[0] < self.ySize and 0 <= coord1[
            1] < self.xSize:
            diffVector = coord1 - coord0
            absTotal = abs(diffVector[0]) + abs(diffVector[1])
            return diffVector, 1 if absTotal == 3 and diffVector[0] != 0 and diffVector[1] != 0 else (
                (diffVector / (absTotal / 2)).astype(int), int(absTotal / 2)) if abs(diffVector[0]) == abs(
                diffVector[1]) else ((diffVector / absTotal).astype(int), absTotal) if absTotal == abs(
                diffVector[0]) or absTotal == abs(diffVector[1]) else None
        return None


def arrayInList(arr: npt.NDArray[Any], lst: list[npt.NDArray[Any]]) -> bool:
    """
    checks if an array is in a list of arrays and returns a bool
    :param arr: array to check for
    :param lst: list of arrays to check
    :return:
    """
    return False if lst is None else any(np.array_equal(arr, elem) for elem in lst)


def indexOfArrayInList(arr: npt.NDArray[Any], lst: list[npt.NDArray[Any]]) -> int | None:
    """
    finds the index of an array is in a list of arrays
    :param arr: array to find the index of
    :param lst: list of arrays to check
    :return:
    """
    if lst is None:
        return None
    for i in range(len(lst)):
        if np.array_equal(arr, lst[i]):
            return i
    return None


def removeArray(arr: npt.NDArray[Any], lst: list[npt.NDArray[Any]]) -> None:
    """
    removes an array from a list of arrays
    :param arr: array to remove
    :param lst: list of arrays to remove from
    :return:
    """
    if arrayInList(arr, lst):
        ind = 0
        size = len(lst)
        while ind != size and not np.array_equal(lst[ind], arr):
            ind += 1
        if ind != size:
            lst.pop(ind)
