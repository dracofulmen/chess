import random
from typing import Any, Callable, Optional
from piece import Piece
from piece import King
import errors
import numpy as np
import numpy.typing as npt
from collections import Counter
from board import Board, arrayInList, indexOfArrayInList, removeArray


class Chess960Board(Board):
    def defaultStart(self) -> list[str]:
        """
        starting board layout
        :return:
        """
        blackSquareBishop = 2 * random.randrange(4)
        whiteSquareBishop = 2 * random.randrange(4) + 1
        rookSeenNum = 0
        firstRowList = ['q', 'r', 'r', 'r', 'n', 'n']
        firstRowCastleList = []
        random.shuffle(firstRowList)
        for i in range(8):
            if i == blackSquareBishop or i == whiteSquareBishop:
                firstRowList.insert(i, 'b')
            elif firstRowList[i] == 'r':
                firstRowCastleList.append(i)
                if rookSeenNum == 1:
                    firstRowList[i] = 'k'
                rookSeenNum += 1
        firstRowString = ''.join(firstRowList)
        lastRowString = firstRowString.upper()[::-1]
        self.startCastlingLocationDict = {
            -1: np.array([[firstRowCastleList[0], 0], [[firstRowCastleList[1]], 4], [firstRowCastleList[2], 7]]),
            1: np.array([[firstRowCastleList[2], 0], [firstRowCastleList[1], 4], [firstRowCastleList[0], 7]])}
        return [firstRowString + "/pppppppp/8/8/8/8/PPPPPPPP/" + lastRowString, 'w', "KQkq", '-', '0', '1']

    @property
    def startCastlingLocationDict(self) -> dict[int, npt.NDArray | None]:
        """
        dictionary for rook and king initial locations (order is queen side rook, king, king side rook)
        :return:
        """
        return self._startCastlingLocationDict

    @startCastlingLocationDict.setter
    def startCastlingLocationDict(self, startCastlingLocationDict: dict[int, npt.NDArray | None]) -> None:
        self._startCastlingLocationDict = startCastlingLocationDict

    def validCastleOptions(self, color: int, useCheck: bool = None) -> list[npt.NDArray[int]]:
        """
        returns a list of moves that are valid and perform a castle (uses rook position, not final position, to prevent overlap)
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
                        retList.append(rookStartCoord)
        return retList

    def updateMoves(self, startCoord: npt.NDArray[int], endCoord: npt.NDArray[int], promotionType: str = None) -> None:
        """
        moves a piece from one location to another and updates all lists
        :param startCoord: starting coordinates of the piece to move
        :param endCoord: ending coordinates of the piece to move
        :param promotionType: type of piece to promote a pawn moving to opponent's end row to (defaults to queen)
        :return:
        """
        curEndCoord = endCoord.copy()
        pieceType = self.typeAt(startCoord)
        color = self.colorAt(startCoord)
        if pieceType == 'p' or color * self.colorAt(endCoord) == -1:
            self.halfMoveNum = 0
        else:
            self.halfMoveNum += 1
        if pieceType == 'k' and arrayInList(endCoord, self.validCastleOptions(color)):
            self.castleChecks[color][1] = False
            self.castleChecks[color][0 if endCoord[1] == self.startCastlingLocationDict[color][1] else 2] = False
            rookStartCoord = self.startCastlingLocationDict[0 if endCoord[1] == 2 else 2]
            rookEndCoord = np.array([startCoord[0], 3]) if endCoord[1] == 2 else np.array(
                [startCoord[0], self.xSize - 3])
            self.removePieceAt(rookStartCoord)
            self.addPieceAt(rookEndCoord, 'r', color)
            curEndCoord = np.array([self.nthRowForColor(0, color),
                                    2 if endCoord[1] == self.startCastlingLocationDict[color][1] else self.xSize - 2])
        elif pieceType == 'p' and self.usesEPAtAll and self.usesEP(startCoord, endCoord):
            self.removePieceAt(np.array((self.epCoord[0] - color, self.epCoord[1])))
        elif (pieceType == 'k' or pieceType == 'r') and self.nthRowForColor(0, color):
            posList = [square[1] for square in self.startCastlingLocationDict[color]]
            if startCoord[1] in posList:
                self.castleChecks[color][posList.index(startCoord[1])] = False
        self.removePieceAt(startCoord)
        if pieceType == 'p' and endCoord[0] == self.nthRowForColor(self.promotionRow, color):
            self.addPieceAt(curEndCoord, promotionType, color) if promotionType else self.addPieceAt(endCoord, 'q',
                                                                                                     color)
        else:
            self.addPieceAt(curEndCoord, pieceType, color)
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
