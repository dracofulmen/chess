class InvalidMoveBlocked(Exception):
    def __init__(self, message="Invalid move due to occupied square in the way"):
        self.message = message
        super().__init__(self.message)


class InvalidMoveOffBoard(Exception):
    def __init__(self, message="Invalid move due to being off of the board"):
        self.message = message
        super().__init__(self.message)


class InvalidMoveIntoCheck(Exception):
    def __init__(self, message="Invalid move due to being into check"):
        self.message = message
        super().__init__(self.message)


class InvalidMoveCheck(Exception):
    def __init__(self, message="Invalid move due to being into check"):
        self.message = message
        super().__init__(self.message)


class InvalidMoveCastle(Exception):
    def __init__(self, message="Invalid move due to inability to castle"):
        self.message = message
        super().__init__(self.message)


class InvalidMoveWrongColor(Exception):
    def __init__(self, message="Invalid move due to wrong color"):
        self.message = message
        super().__init__(self.message)


class InvalidMoveGeneric(Exception):
    def __init__(self, message="Invalid move"):
        self.message = message
        super().__init__(self.message)


class PieceCantMove(Exception):
    def __init__(self, message="This piece can't move"):
        self.message = message
        super().__init__(self.message)


class InvalidSyntax(Exception):
    def __init__(self, message="Invalid syntax"):
        self.message = message
        super().__init__(self.message)


class GameOver(Exception):
    def __init__(self, winner: int, message="Game Over. "):
        self.message = message
        match winner:
            case 1:
                self.message += "White won."
            case 0:
                self.message += "Draw."
            case -1:
                self.message += "Black won."
        super().__init__(self.message)
