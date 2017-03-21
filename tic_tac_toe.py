import random
import time

import matplotlib.pyplot as plt
import numpy as np


def random_place(board, player):
    possibilities = [tuple(i) for i in np.transpose(np.where(board == 0))]
    board[random.choice(possibilities)] = player


def evaluate(board, player):
    rows = np.any([np.all([row == player]) for row in board])
    columns = np.any([np.all([row == player]) for row in board.transpose()])
    diagonal1 = np.all([board.diagonal() == player])
    diagonal2 = np.all([np.fliplr(board).diagonal() == player])
    if np.any([rows, columns, diagonal1, diagonal2]):
        winner = player
    elif np.all([board != 0]):
        winner = 0
    else:
        winner = -1
    return winner


def play_game(strategic=False):
    board, winner = np.zeros((3, 3)), -1
    if not strategic:
        turn = 0
    else:
        turn = 1
        board[1, 1] = 1
    while winner == -1:
        random_place(board, turn % 2 + 1)
        winner = evaluate(board, turn % 2 + 1)
        turn += 1
    return winner


games = 1000

start_time = time.time()
normal_games = [play_game() for i in range(games)]
end_time = time.time()
normal_time = np.round(end_time - start_time, 2)

start_time = time.time()
strategic_games = [play_game(True) for j in range(games)]
end_time = time.time()
strategic_time = np.round(end_time - start_time, 2)

plt.hist(normal_games, bins=(-0.5, 0.01, 0.5, 1.01, 1.5, 2.01),
         label="Normal time: " + str(normal_time) + "s")
plt.hist(strategic_games, bins=(0, 0.5, 1, 1.5, 2, 2.5), color='g',
         label="Strategic time: " + str(strategic_time) + "s")
plt.legend(loc='upper left')
plt.title("Normal Vs Strategic " + str(games) + " games")
plt.savefig('plots/tic_tac_toe')
plt.show()
