from pytest import mark, raises
from quarto import Game, Piece, PIECES, HIGH, LOW, LIGHT, DARK, ROUND, SQUARE, SOLID, HOLLOW

def test_is_win_default():
    game = Game()
    assert not game.is_win()

@mark.parametrize("trait", [LOW, HIGH])
@mark.parametrize("col", range(4))
def test_is_win_col_of_same_trait(trait, col):
    game = Game()
    game.place(Piece(trait, LIGHT, ROUND, SOLID), 0, col)
    game.place(Piece(trait, LIGHT, SQUARE, SOLID), 1, col)
    game.place(Piece(trait, DARK, ROUND, SOLID), 2, col)
    game.place(Piece(trait, DARK, SQUARE, SOLID), 3, col)
    assert game.is_win()

@mark.parametrize("trait", [LOW, HIGH])
@mark.parametrize("col", range(4))
def test_is_win_row_of_same_trait(trait, col):
    game = Game()
    game.place(Piece(trait, LIGHT, ROUND, SOLID), col, 0)
    game.place(Piece(trait, LIGHT, SQUARE, SOLID), col, 1)
    game.place(Piece(trait, DARK, ROUND, SOLID), col, 2)
    game.place(Piece(trait, DARK, SQUARE, SOLID), col, 3)
    assert game.is_win()


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


def test_high_pieces():
    assert len(PIECES) == 16
    for i in range(8):
        assert PIECES[i].is_(HIGH)
        assert not PIECES[i].is_(LOW)


def test_low_pieces():
    assert len(PIECES) == 16
    for i in range(9, 16):
        assert PIECES[i].is_(LOW)
        assert not PIECES[i].is_(HIGH)


def test_invalid_placement_on_non_empty_position():
    game = Game()
    game.place(Piece(HIGH, LIGHT, ROUND, SOLID), 0, 0)
    with raises(ValueError):
        game.place(Piece(HIGH, LIGHT, ROUND, SOLID), 0, 0)


def test_invalid_placement_of_duplicate_piece():
    game = Game()
    game.place(Piece(HIGH, LIGHT, ROUND, SOLID), 0, 0)
    with raises(ValueError):
        game.place(Piece(HIGH, LIGHT, ROUND, SOLID), 1, 1)
