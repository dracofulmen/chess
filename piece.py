import numpy as np
import numpy.typing as npt


class Piece:

    def __init__(self, pieceType: str | None, color: int | None, moveList: list = None, blockList: list = None,
                 captureList: list = None):
        """
        init
        :param pieceType: p=pawn, r=rook, n=knight, b=bishop, k=king, q=queen
        :param color: 1=white, -1=black, 0=none
        :param moveList: custom move list; defaults to None
        :param blockList: custom block list; defaults to None
        :param captureList: custom capture list; defaults to None

        """
        self.pieceType, self.color, self.moveList, self.blockList, self.captureList = pieceType, color, moveList, blockList, captureList

        if self.moveList is None:
            self.moveList = []
        if self.blockList is None:
            self.blockList = []
        if self.captureList is None:
            self.captureList = []

    def __str__(self):
        return str(self.pieceType) + str(self.color)

    def __bool__(self) -> bool:
        """
        checks if the piece exists (if it has a type and a color)
        :return:
        """
        if self.pieceType is not None and self.color != 0:
            return True
        else:
            return False

    def char(self) -> str:
        """
        gives the unicode character for the piece
        :return: unicode character for the piece or None if empty
        """
        charDict = {'k1': '\u2654', 'q1': '\u2655', 'r1': '\u2656', 'b1': '\u2657', 'n1': '\u2658', 'p1': '\u2659',
                    'k-1': '\u265a', 'q-1': '\u265b', 'r-1': '\u265c', 'b-1': '\u265d', 'n-1': '\u265e',
                    'p-1': '\u265f',
                    "None0": " "}
        return charDict[str(self)]


class King:
    def __init__(self, inCheck: bool, position: npt.NDArray):
        self.inCheck, self.position = inCheck, position
