from board import Board, arrayInList, indexOfArrayInList, removeArray


class NoCastlingBoard(Board):
    @staticmethod
    def defaultStart() -> list[str]:
        """
        starting board layout
        :return:
        """
        return ["rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", 'w', "-", '-', '0', '1']

    @property
    def usesCastling(self) -> bool:
        """
        bool specifying whether castling is used
        :return:
        """
        return False
