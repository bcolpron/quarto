import random
from quarto import Game, Player
import ai_1 as player1
import ai_2 as player2

game = Game(
    Player.from_module(player1),
    Player.from_module(player2))
game.play()
