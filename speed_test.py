from board import Board
import time

# Before 12 seconds with 100_000

start_time = time.time()
n = 100_000

board = Board()
for i in range(n):
    for x,y in board.get_player_positions(1):
        board.get_legal_moves(x,y)

print(time.time() - start_time)
