import cProfile
from ai import AI
from board import Board
import random
from mcts import Tree, Node

def legal_moves():
    board = Board()
    for i in range(10000):
        for x,y in board.get_player_positions(1):
            board.get_legal_moves(x,y)

def main():
    board = Board()
    ai1 = AI(1, board)
    ai2 = AI(2, board)

    explore = 20 / 100

    root = Node("Start")
    tree1 = Tree(root)
    moves = []
    board.reset()
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
        tree1.add_game(moves, board.is_won()==1)
    

cProfile.run('legal_moves()')
