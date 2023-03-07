from pytest import mark, raises
from quarto import Board, Piece, Game, Player, PIECES, HIGH, LOW, LIGHT, DARK, ROUND, SQUARE, SOLID, HOLLOW

def test_is_win_default():
    board = Board()
    assert not board.is_win()

@mark.parametrize("trait", [LOW, HIGH])
@mark.parametrize("col", range(4))
def test_is_win_col_of_same_trait(trait, col):
    board = Board()
    board.place(Piece(trait, LIGHT, ROUND, SOLID), 0, col)
    board.place(Piece(trait, LIGHT, SQUARE, SOLID), 1, col)
    board.place(Piece(trait, DARK, ROUND, SOLID), 2, col)
    board.place(Piece(trait, DARK, SQUARE, SOLID), 3, col)
    assert board.is_win()

@mark.parametrize("trait", [LOW, HIGH])
@mark.parametrize("col", range(4))
def test_is_win_row_of_same_trait(trait, col):
    board = Board()
    board.place(Piece(trait, LIGHT, ROUND, SOLID), col, 0)
    board.place(Piece(trait, LIGHT, SQUARE, SOLID), col, 1)
    board.place(Piece(trait, DARK, ROUND, SOLID), col, 2)
    board.place(Piece(trait, DARK, SQUARE, SOLID), col, 3)
    assert board.is_win()


def test_is_win_diagonal():
    board = Board()
    board.place(Piece(LOW, LIGHT, ROUND, SOLID), 0, 0)
    board.place(Piece(LOW, LIGHT, SQUARE, SOLID), 1, 1)
    board.place(Piece(LOW, DARK, ROUND, SOLID), 2, 2)
    board.place(Piece(LOW, DARK, SQUARE, SOLID), 3, 3)
    assert board.is_win()


def test_is_win_diagonal2():
    board = Board()
    board.place(Piece(LOW, LIGHT, ROUND, SOLID), 0, 3)
    board.place(Piece(LOW, LIGHT, SQUARE, SOLID), 1, 2)
    board.place(Piece(LOW, DARK, ROUND, SOLID), 2, 1)
    board.place(Piece(LOW, DARK, SQUARE, SOLID), 3, 0)
    assert board.is_win()


def test_draw():
    board = Board()
    board.place(Piece(HIGH, DARK,  ROUND,  HOLLOW),  0, 0)
    board.place(Piece(LOW, LIGHT, ROUND,  SOLID), 0, 1)
    board.place(Piece(HIGH,  DARK, SQUARE, HOLLOW),  0, 2)
    board.place(Piece(HIGH, LIGHT,  SQUARE, HOLLOW), 0, 3)
    board.place(Piece(LOW,  DARK,  ROUND,  HOLLOW),  1, 0)
    board.place(Piece(HIGH, LIGHT,  SQUARE,  SOLID), 1, 1)
    board.place(Piece(HIGH, LIGHT,  ROUND, SOLID),  1, 2)
    board.place(Piece(LOW, DARK, ROUND, SOLID), 1, 3)
    board.place(Piece(HIGH, DARK, SQUARE,  SOLID),  2, 0)
    board.place(Piece(LOW,  DARK, SQUARE,  HOLLOW), 2, 1)
    board.place(Piece(LOW, LIGHT, ROUND, HOLLOW),  2, 2)
    board.place(Piece(HIGH,  DARK,  ROUND, SOLID), 2, 3)
    board.place(Piece(LOW, LIGHT,  SQUARE, SOLID),  3, 0)
    board.place(Piece(HIGH,  LIGHT,  ROUND,  HOLLOW), 3, 1)
    board.place(Piece(LOW, LIGHT,  SQUARE,  HOLLOW),  3, 2)
    board.place(Piece(LOW,  DARK, SQUARE, SOLID), 3, 3)
    assert not board.is_win()
    assert board.is_end()


@mark.parametrize("trait", [0, "whatever", None, {}, [], 10000])
def test_piece_ctor_invalid_traits(trait):
    with raises(ValueError):
        Piece(LOW, LIGHT, ROUND, trait)


@mark.parametrize("traits", [
    [LOW, LOW, LOW, LOW],
    [LOW, HIGH, ROUND, SOLID],
    [DARK, LIGHT, ROUND, SOLID],
    [LOW, LIGHT, ROUND, SQUARE],
    [LOW, LIGHT, HOLLOW, SOLID],
])
def test_piece_ctor_invalid_piece(traits):
    with raises(ValueError):
        Piece(*traits)


def test_piece_equality():
    assert Piece(HIGH, LIGHT, ROUND, SOLID) == Piece(HIGH, LIGHT, ROUND, SOLID)
    assert Piece(HIGH, LIGHT, ROUND, SOLID) != Piece(LOW, LIGHT, ROUND, SOLID)


def test_piece_equality_with_none():
    assert Piece(HIGH, LIGHT, ROUND, SOLID) != None


def test_piece_stringification():
    assert str(Piece(HIGH, LIGHT, ROUND, SOLID)) == "Piece(HIGH, LIGHT, ROUND, SOLID)"
    assert repr(Piece(HIGH, LIGHT, ROUND, SOLID)) == "Piece(HIGH, LIGHT, ROUND, SOLID)"


def test_piece_traits():
    assert Piece(HIGH, DARK, ROUND, HOLLOW).traits() == (HIGH, DARK, ROUND, HOLLOW)
    assert Piece(LOW, LIGHT, SQUARE, SOLID).traits() == (LOW, LIGHT, SQUARE, SOLID)


def test_piece_short_name():
    assert Piece(HIGH, LIGHT, ROUND,  SOLID  ).short_name() == "A"
    assert Piece(HIGH, LIGHT, ROUND,  HOLLOW ).short_name() == "B"
    assert Piece(HIGH, LIGHT, SQUARE, SOLID  ).short_name() == "C"
    assert Piece(HIGH, LIGHT, SQUARE, HOLLOW ).short_name() == "D"
    assert Piece(HIGH, DARK,  ROUND,  SOLID  ).short_name() == "E"
    assert Piece(HIGH, DARK,  ROUND,  HOLLOW ).short_name() == "F"
    assert Piece(HIGH, DARK,  SQUARE, SOLID  ).short_name() == "G"
    assert Piece(HIGH, DARK,  SQUARE, HOLLOW ).short_name() == "H"
    assert Piece(LOW,  LIGHT, ROUND,  SOLID  ).short_name() == "I"
    assert Piece(LOW,  LIGHT, ROUND,  HOLLOW ).short_name() == "J"
    assert Piece(LOW,  LIGHT, SQUARE, SOLID  ).short_name() == "K"
    assert Piece(LOW,  LIGHT, SQUARE, HOLLOW ).short_name() == "L"
    assert Piece(LOW,  DARK,  ROUND,  SOLID  ).short_name() == "M"
    assert Piece(LOW,  DARK,  ROUND,  HOLLOW ).short_name() == "N"
    assert Piece(LOW,  DARK,  SQUARE, SOLID  ).short_name() == "O"
    assert Piece(LOW,  DARK,  SQUARE, HOLLOW ).short_name() == "P"


def test_high_pieces():
    assert len(PIECES) == 16
    for i in range(8):
        assert PIECES[i].has(HIGH)
        assert not PIECES[i].has(LOW)


def test_low_pieces():
    assert len(PIECES) == 16
    for i in range(9, 16):
        assert PIECES[i].has(LOW)
        assert not PIECES[i].has(HIGH)


def test_invalid_placement_on_non_empty_position():
    board = Board()
    board.place(Piece(HIGH, LIGHT, ROUND, SOLID), 0, 0)
    with raises(ValueError):
        board.place(Piece(HIGH, LIGHT, ROUND, SOLID), 0, 0)


def test_invalid_placement_of_duplicate_piece():
    board = Board()
    board.place(Piece(HIGH, LIGHT, ROUND, SOLID), 0, 0)
    with raises(ValueError):
        board.place(Piece(HIGH, LIGHT, ROUND, SOLID), 1, 1)


def test_available_defaults():
    board = Board()
    assert len(board.available_pieces()) == 16
    assert all([board[x,y] is None for x in range(4) for y in range(4)])


def test_available_pieces_place():
    board = Board()
    p = Piece(HIGH, LIGHT, ROUND, SOLID)
    board.place(p, 0, 0)
    assert len(board.available_pieces()) == 15
    assert p not in board.available_pieces()
    

def test_index_operator():
    board = Board()
    p = board.available_pieces()[0]
    board.place(p, 0, 0)
    assert board[0,0] == p


def test_index_operator_invalid_inputs():
    board = Board()
    with raises(ValueError):
        board[0]
    with raises(ValueError):
        board[::1]
    with raises(ValueError):
        board[0,0,0]
    with raises(ValueError):
        board[-1, 0]
    with raises(ValueError):
        board[5, 0]
    with raises(ValueError):
        board[0, -1]
    with raises(ValueError):
        board[0, 5]
    with raises(ValueError):
        board[0.1, 3.3]

def test_game_play():
    def f(piece, board):
        positions = [(x,y) for x in range(4) for y in range(4)]
        pos = next((pos for pos in positions if board[pos] is None))
        return pos, board.available_pieces()[0]

    player = Player("Bob", f)

    game = Game(player, player)
    game.play()
    assert game._board.is_win() is True
