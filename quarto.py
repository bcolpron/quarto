from enum import Enum, IntEnum
from functools import reduce

class Trait(IntEnum):
    LOW = 1
    HIGH = 2
    LIGHT = 4
    DARK = 8
    ROUND = 16
    SQUARE = 32
    SOLID = 64
    HOLLOW = 128

# For convenience
LOW = Trait.LOW
HIGH = Trait.HIGH
LIGHT = Trait.LIGHT
DARK = Trait.DARK
ROUND = Trait.ROUND
SQUARE = Trait.SQUARE
SOLID = Trait.SOLID
HOLLOW = Trait.HOLLOW

TRAITS = [HIGH, LOW, LIGHT, DARK, ROUND, SQUARE, SOLID, HOLLOW]

class Piece:
    def __init__(self, t1, t2, t3, t4):
        traits = [t1, t2, t3, t4]
        for t in traits:
            if t not in TRAITS:
                raise ValueError("invalid piece traits")
        
        if any(traits.count(x) > 1 for x in traits):
            raise ValueError("invalid piece trait combo")

        self._traits = reduce(lambda x, y: x|y, traits)

        if self.has(HIGH) and self.has(LOW) \
            or self.has(LIGHT) and self.has(DARK) \
            or self.has(ROUND) and self.has(SQUARE) \
            or self.has(SOLID) and self.has(HOLLOW):
            raise ValueError("invalid trait combination")

    def has(self, trait):
        return self._traits & trait == trait

    def __eq__(self, piece):
        return piece is not None and self._traits == piece._traits

    def __repr__(self):
        t = [Trait(x).name for x in TRAITS if self.has(x)]
        return f"Piece({t[0]}, {t[1]}, {t[2]}, {t[3]})"

PIECES = [
    Piece(HIGH, LIGHT, ROUND,  SOLID  ),
    Piece(HIGH, LIGHT, ROUND,  HOLLOW ),
    Piece(HIGH, LIGHT, SQUARE, SOLID  ),
    Piece(HIGH, LIGHT, SQUARE, HOLLOW ),
    Piece(HIGH, DARK,  ROUND,  SOLID  ),
    Piece(HIGH, DARK,  ROUND,  HOLLOW ),
    Piece(HIGH, DARK,  SQUARE, SOLID  ),
    Piece(HIGH, DARK,  SQUARE, HOLLOW ),
    Piece(LOW,  LIGHT, ROUND,  SOLID  ),
    Piece(LOW,  LIGHT, ROUND,  HOLLOW ),
    Piece(LOW,  LIGHT, SQUARE, SOLID  ),
    Piece(LOW,  LIGHT, SQUARE, HOLLOW ),
    Piece(LOW,  DARK,  ROUND,  SOLID  ),
    Piece(LOW,  DARK,  ROUND,  HOLLOW ),
    Piece(LOW,  DARK,  SQUARE, SOLID  ),
    Piece(LOW,  DARK,  SQUARE, HOLLOW ) ]

class Game:

    def __init__(self):
        self._board = [[None]*4, [None]*4, [None]*4, [None]*4]

    def is_win(self):
        for trait in TRAITS:
            def matches(cell):
                return cell is not None and cell.has(trait)

            for i in range(4):
                if all([matches(self._board[j][i]) for j in range(4)]):
                    return True
                if all([matches(self._board[i][j]) for j in range(4)]):
                    return True
            if all([matches(self._board[i][i]) for i in range(4)]):
                    return True
            if all([matches(self._board[3-i][i]) for i in range(4)]):
                    return True
        return False

    def place(self, piece: Piece, row: int, col: int):
        if self._board[row][col] is not None:
            raise ValueError("place already occupied")
        if any([self._board[r][c] == piece for r in range(4) for c in range(4)]):
            raise ValueError("piece already present")
        self._board[row][col] = piece