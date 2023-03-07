from random import choice
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

    def traits(self):
        return (HIGH if self.has(HIGH) else LOW,
                LIGHT if self.has(LIGHT) else DARK,
                ROUND if self.has(ROUND) else SQUARE,
                SOLID if self.has(SOLID) else HOLLOW)

    def short_name(self):
        index = (8 if self.has(LOW) else 0) \
            + (4 if self.has(DARK) else 0) \
            + (2 if self.has(SQUARE) else 0) \
            + (1 if self.has(HOLLOW) else 0)
        return "ABCDEFGHIJKLMNOP"[index]

    def __eq__(self, piece):
        return piece is not None and self._traits == piece._traits

    def __repr__(self):
        t = [Trait(x).name for x in TRAITS if self.has(x)]
        return f"Piece({t[0]}, {t[1]}, {t[2]}, {t[3]})"

PIECES = (
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
    Piece(LOW,  DARK,  SQUARE, HOLLOW ) )

class Board:

    def __init__(self):
        self._board = [[None]*4, [None]*4, [None]*4, [None]*4]
        self._available_pieces = list(PIECES)

    def available_pieces(self):
        return self._available_pieces.copy()

    def __getitem__(self, key):
        if not isinstance(key, tuple) or len(key) != 2 \
            or not isinstance(key[0], int) or not isinstance(key[1], int) \
            or not (0 <= key[0] < 4 and 0 <= key[1] < 4):
            raise ValueError("index must be 2-tuple of int in [0, 3]")
        return self._board[key[0]][key[1]]

    def is_end(self):
        return len(self._available_pieces) == 0

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
        self._available_pieces.remove(piece)

class Game:

    PLAYER_1_WINS = 1
    PLAYER_2_WINS = 2
    DRAW = 0

    def __init__(self, player1, player2):
        self._board = Board()
        self._player1 = player1
        self._player2 = player2
        self._turn = choice(range(2))

    def next_player(self):
        self._turn = (self._turn + 1) % 2
        return self._player1 if self._turn == 0 else self._player2

    def play(self):
        p = choice(self._board.available_pieces())
        while(not self._board.is_end() and not self._board.is_win()):
            player = self.next_player()
            pos, p = player.play(p, self._board)
            self._board.place(p, *pos)
        if self._board.is_win():
            return self.PLAYER_1_WINS if self._turn == 0 else self.PLAYER_2_WINS
        else:
            return self.DRAW

class Player:
    def __init__(self, name, func):
        self.name = name
        self.play = func

    @staticmethod
    def from_module(mod):
        return Player(mod.__name__, mod.play)