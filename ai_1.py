import random
from quarto import Game

def available_positions(board):
    positions = [(x,y) for x in range(4) for y in range(4)]
    return [pos for pos in positions if board[pos] is None]


def play(piece_to_place, board):

    # Pick a random free position
    position = random.choice(available_positions(board))
    
    # Piece a piece to give the opponent
    next_piece = random.choice(board.available_pieces()) if not board.is_end() else None
    
    return position, next_piece
