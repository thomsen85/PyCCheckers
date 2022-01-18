from ai import AI
from board import Board
import random
from rich import print
from rich.progress import track
from mcts import Tree, Node
import time
from concurrent.futures import ThreadPoolExecutor
import concurrent

WORKERS = 50

explore = 20/100

root = Node("Start")
tree1 = Tree(root)

start_time = time.time()


def get_game(game):
    board = Board()
    ai1 = AI(1, board)
    ai2 = AI(2, board)
    moves = []
    rounds = 0
    while not board.is_won() and rounds < 450:
        if random.random() < explore:
            ai1_move = ai1.make_closer_move((12, 26))
        else:
            ai1_move = ai1.make_random_move()

        if random.random() > explore:
            ai2_move = ai2.make_closer_move((12, 0))
        else:
            ai2_move = ai2.make_random_move()

        moves.extend([ai1_move, ai2_move])
        rounds += 1

    print(board.is_won())
    return moves, board.is_won()


def main():
    print("Fetching...")
    processes = []
    with ThreadPoolExecutor(max_workers=None) as executor:
        processes.append(executor.map(get_game, [0]*100))

        for _ in concurrent.futures.as_completed(processes):
            print('Result: ', _.result())


if __name__ == "__main__":
    main()
    print("Time taken: ", time.time() - start_time)




#tree1.add_game(moves, board.is_won()==1)

#tree1.get_visualization(root, 1)
