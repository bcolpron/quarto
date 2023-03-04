import random
from quarto import Game

def available_positions(board):
    positions = [(x,y) for x in range(4) for y in range(4)]
    return [pos for pos in positions if board[pos] is None]


def play(piece_to_place, board):

    # Pick next available position
    position = available_positions(board)[0]
    
    # Piece a piece to give the opponent
    next_piece = board.available_pieces()[0] if not board.is_end() else None
    
    return position, next_piece
