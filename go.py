import random
from quarto import Game, Player
import ai_1 as player1
import ai_3 as player2

PLAYER1=Player.from_module(player1)
PLAYER2=Player.from_module(player2)

def play_game():
    game = Game(PLAYER1, PLAYER2)
    return game.play()

def play_games(n):
    p1_wins = 0
    p2_wins = 0
    for i in range(n):
        outcome = play_game()
        if outcome == Game.PLAYER_1_WINS:
            p1_wins += 1
        elif outcome == Game.PLAYER_2_WINS:
            p2_wins += 1
    print (f"Player {PLAYER1.name} won {p1_wins} times")
    print (f"Player {PLAYER2.name} won {p2_wins} times")
    print (f"{n-p1_wins-p2_wins} draws")

play_games(100)