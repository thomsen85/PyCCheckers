import copy
import math
from typing import Tuple

from board import Board


class MinimaxPlayer:
    """
    A player that makes moves based on the minimax algorithm.

    ONLY works for two players.
    It evals a positon based on the distance from the goal and if it has won or not.
    """

    def __init__(self, player_nr, max_depth=3):
        self.player_nr = player_nr
        self.max_depth = max_depth

        self.other_player = Board.PLAYER_2_NR if player_nr == Board.PLAYER_1_NR else Board.PLAYER_1_NR

    def get_best_move(self, board):
        """Gets the best move from the current board state, does not check if it is its own turn."""
        eval, best_move = self._minimax(
            board, self.max_depth, float("-inf"), float("inf"), True
        )
        print(eval)
        return best_move

    def _eval_position(self, board: Board):
        """Evaluates the position of the board for the given player_nr"""
        if board.is_won() == self.player_nr:
            return float("inf")
        elif board.is_won() > 0:
            return float("-inf")

        player_goal_y = board.HEIGHT if self.player_nr == Board.PLAYER_1_NR else 0
        other_goal_y = board.HEIGHT if self.player_nr != Board.PLAYER_1_NR else 0
        mid = Board.WIDTH // 2

        dist = 0
        for x, y in board.get_player_positions(self.player_nr):
            dist += (player_goal_y - y)**2 + (mid - x)**2

        other_dist = 0
        for x, y in board.get_player_positions(self.other_player):
            other_dist += (other_goal_y - y)**2 + (mid - x)**2

        return other_dist - dist

    def _minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_won() != 0:
            return self._eval_position(board), None

        if maximizing_player:
            max_eval = float("-inf")
            best_move = None
            for move in board.get_all_legal_moves_by_player(self.player_nr):
                new_board = copy.deepcopy(board)
                x, y, to_x, to_y = move
                new_board.move(x, y, to_x, to_y)
                eval, _ = self._minimax(new_board, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float("inf")
            best_move = None
            for move in board.get_all_legal_moves_by_player(self.other_player):
                new_board = copy.deepcopy(board)
                x, y, to_x, to_y = move
                new_board.move(x, y, to_x, to_y)
                eval, _ = self._minimax(new_board, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move
