from enum import IntEnum
from functools import reduce

LOW = 1
HIGH = 2
LIGHT = 4
DARK = 8
ROUND = 16
SQUARE = 32
SOLID = 64
HOLLOW = 128

TRAITS = [HIGH, LOW, LIGHT, DARK, ROUND, SQUARE, SOLID, HOLLOW]


class Piece:
    def __init__(self, t1, t2, t3, t4):
        traits = [t1, t2, t3, t4]
        for t in traits:
            if t not in TRAITS:
                raise ValueError("invalid piece traits")
        
        self._traits = reduce(lambda x, y: x|y, traits)

        if self.is_(HIGH) and self.is_(LOW):
            raise ValueError("invalid trait combination")

    def is_(self, trait):
        return self._traits & trait == trait

    def __eq__(self, piece):
        return piece is not None and self._traits == piece._traits

PIECES = [
    Piece(HIGH , LIGHT , ROUND  , SOLID  ),
    Piece(HIGH , LIGHT , ROUND  , HOLLOW ),
    Piece(HIGH , LIGHT , SQUARE , SOLID  ),
    Piece(HIGH , LIGHT , SQUARE , HOLLOW ),
    Piece(HIGH , DARK  , ROUND  , SOLID  ),
    Piece(HIGH , DARK  , ROUND  , HOLLOW ),
    Piece(HIGH , DARK  , SQUARE , SOLID  ),
    Piece(HIGH , DARK  , SQUARE , HOLLOW ),
    Piece(LOW  , LIGHT , ROUND  , SOLID  ),
    Piece(LOW  , LIGHT , ROUND  , HOLLOW ),
    Piece(LOW  , LIGHT , SQUARE , SOLID  ),
    Piece(LOW  , LIGHT , SQUARE , HOLLOW ),
    Piece(LOW  , DARK  , ROUND  , SOLID  ),
    Piece(LOW  , DARK  , ROUND  , HOLLOW ),
    Piece(LOW  , DARK  , SQUARE , SOLID  ),
    Piece(LOW  , DARK  , SQUARE , HOLLOW ) ]

class Game:

    def __init__(self):
        self._board = [[None]*4, [None]*4, [None]*4, [None]*4]

    def is_win(self):
        for trait in TRAITS:
            for row in range(4):
                if all([x is not None and x.is_(trait) for x in self._board[row]]):
                    return True
            for col in range(4):
                if all([self._board[row][col] is not None and self._board[row][col].is_(trait) for row in range(4)]):
                    return True
        return False

    def place(self, piece: Piece, row: int, col: int):
        if self._board[row][col] is not None:
            raise ValueError("place already occupied")
        if any([self._board[r][c] == piece for r in range(4) for c in range(4)]):
            raise ValueError("piece already present")
        self._board[row][col] = piece